import ast
import json
import logging
import os.path
import re
import time
import traceback
from argparse import ArgumentParser
from datetime import datetime
from functools import reduce

from docker.errors import DockerException, ImageNotFound, APIError
from requests.exceptions import HTTPError
from tqdm import tqdm

logger = logging.getLogger('dockerman')


def _parser():
    _p = ArgumentParser()
    _p.add_argument('--version', action='version', version='dimsync 0.1.0')
    _subs = _p.add_subparsers(dest='command', help='commands')
    # config
    _p_config = _subs.add_parser('config', help='get or set config')
    _subs_config = _p_config.add_subparsers(dest='subcommand', help='subcommand')
    _subs_config.add_parser('ls')
    _p_config_get = _subs_config.add_parser('get')
    _p_config_get.add_argument('key')
    _p_config_set = _subs_config.add_parser('set')
    _p_config_set.add_argument('key')
    _p_config_set.add_argument('value')
    _p_config_unset = _subs_config.add_parser('unset')
    _p_config_unset.add_argument('key')
    _p_config_add = _subs_config.add_parser('add')
    _p_config_add.add_argument('key')
    _p_config_add.add_argument('value')
    _p_config_del = _subs_config.add_parser('del')
    _p_config_del.add_argument('key')
    _p_config_del.add_argument('value')
    # fetch
    _p_fetch = _subs.add_parser('fetch', help='fetch updates')
    _p_fetch.add_argument('pattern', nargs='?', help='name or pattern')
    # sync
    _p_sync = _subs.add_parser('sync', help='push updates to registry')
    _p_sync.add_argument('pattern', nargs='?', help='name or pattern')
    _p_sync.add_argument('registry', nargs='?', help='registry')
    # prune
    _p_prune = _subs.add_parser('prune', help='clean orphan images')
    _p_prune.add_argument('-f', '--force', action='store_true', help='also clean stopped containers')
    return _p


def _help():
    _parser().print_help()


def _data_dir():
    return os.path.expanduser('~/.docker')


class Config(object):
    def __init__(self):
        self.data = {}
        file = os.path.join(_data_dir(), 'dm_config')
        if not os.path.isfile(file):
            return
        with open(file, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict):
            self.data = data

    @property
    def retry(self):
        return self.get('retry', 3)

    @property
    def registry(self):
        return self.get('registry', None)

    def debug(self):
        return bool(ast.literal_eval(self.get('debug', 'False')))

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def save(self):
        os.makedirs(_data_dir(), exist_ok=True)
        file = os.path.join(_data_dir(), 'dm_config')
        with open(file, 'w') as f:
            json.dump(self.data, f, indent=4)


class Cache(object):
    def __init__(self):
        self.data = {}
        file = os.path.join(_data_dir(), 'dm_cache')
        if not os.path.isfile(file):
            return
        with open(file, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict):
            self.data = data
        self.data = {
            k1: {
                k2: {k3: v3 for k3, v3 in v2.items() if all(y != 'None' for y in k3.split('/'))}
                for k2, v2 in v1.items()
                if k2 != 'null'
            }
            for k1, v1 in data.items()
            if k1 != 'null'
        }
        self.save()

    def get(self, **kwargs):
        repo = kwargs.get('repo')
        tag = kwargs.get('tag')
        plat = '{}/{}'.format(kwargs.get('os'), kwargs.get('arch'))
        if repo in self.data and tag in (r := self.data.get(repo)) and plat in (r := r.get(tag)):
            return r.get(plat)
        return None

    def set(self, **kwargs):
        if any(kwargs.get(k) is None for k in ['repo', 'tag', 'os', 'arch']):
            raise ValueError('Error: Missing required arguments')
        keys = [kwargs.get('repo'), kwargs.get('tag'), '{}/{}'.format(kwargs.get('os'), kwargs.get('arch'))]
        value = {k: v for k, v in kwargs.items() if k not in ['repo', 'tag', 'os', 'arch']}
        value.update({'atime': datetime.now().isoformat()})
        reduce(lambda d, k: d.setdefault(k, {}), keys, self.data).update(value)
        self.save()

    def sort(self, images):
        for image in images:
            hist = self.get(**image)
            if hist:
                image['atime'] = hist.get('atime')
                image['exist'] = hist.get('exist', True)
            else:
                image['atime'] = datetime.fromtimestamp(0).isoformat()
        return sorted(images, key=lambda x: datetime.fromisoformat(x['atime']))

    def save(self):
        os.makedirs(_data_dir(), exist_ok=True)
        file = os.path.join(_data_dir(), 'dm_cache')
        with open(file, 'w') as f:
            json.dump(self.data, f, indent=4)


class Docker(object):
    def __init__(self):
        import docker

        self.client = docker.from_env()

    def _image_info(self, image):
        return [
            {
                'repo': x.split(':')[0],
                'tag': x.split(':')[1],
                'os': image.attrs.get('Os'),
                'arch': image.attrs.get('Architecture'),
                'id': image.id.removeprefix('sha256:'),
                'ctime': image.attrs.get('Created'),
                'size': image.attrs.get('Size'),
            }
            for x in image.tags
        ]

    def images(self):
        return [y for x in self.client.images.list() for y in self._image_info(x)]

    def tag(self, src, **kwargs):
        image = self.client.images.get(src)
        if image is None:
            return
        image.tag(kwargs.get('repo'), tag=kwargs.get('tag'))

    def pull(self, **kwargs):
        repo = kwargs.get('repo')
        tag = kwargs.get('tag')
        plat = '{}/{}'.format(kwargs.get('os'), kwargs.get('arch'))
        print(f'Pulling {repo}:{tag}, platform={plat}')
        pull_stream = self.client.api.pull(repo, tag=tag, platform=plat, stream=True, decode=True)
        pull_layers = {}
        pbar = None
        for output in pull_stream:
            if not isinstance(id := output.get('id'), str) or id == tag:
                continue
            pull_layers.setdefault(id, {})
            if isinstance(detail := output.get('progressDetail'), dict):
                pull_layers[id].update(detail)
            if isinstance(status := output.get('status'), str):
                pull_layers[id].update({'status': status})
            complete = sum([1 for v in pull_layers.values() if v.get('status') in ['Already exists', 'Pull complete']])
            current = sum([s for v in pull_layers.values() if isinstance(s := v.get('current'), int)])
            total = sum([s for v in pull_layers.values() if isinstance(s := v.get('total'), int)])
            if total == 0:
                continue
            if pbar is None:
                pbar = tqdm(total=total, unit='B', unit_scale=True, desc='  Pulling', dynamic_ncols=True)
            else:
                pbar.total = total
            pbar.desc = f'  Pulling {complete}/{len(pull_layers)} layers'
            pbar.n = current
            pbar.refresh()
        pbar and pbar.close()
        kwargs.get('debug') and print(pull_layers)
        images = [
            x
            for x in self.client.images.list()
            if f'{repo}:{tag}' in x.tags
            and x.attrs.get('Os') == kwargs.get('os')
            and x.attrs.get('Architecture') == kwargs.get('arch')
        ]
        if len(images) == 0:
            print(f'Error: Image {repo}:{tag} pull failed')
            return
        if len(images) > 1:
            raise ValueError(f'Pull return multiple images: {images}')
        data = [x for x in self._image_info(images[0]) if x.get('repo') == repo and x.get('tag') == tag]
        if len(data) == 0:
            raise ValueError('Pull return empty image')
        elif len(data) > 1:
            raise ValueError(f'Pull return multiple images: {data}')
        data = data[0]
        if kwargs.get('id') != data.get('id'):
            print(f'  Downloaded newer image for {repo}:{tag}')
        else:
            print(f'  Image is up to date for {repo}:{tag}')
        print(f'  Digest: {images[0].id}')
        return data

    def push(self, **kwargs):
        repo = kwargs.get('repo')
        tag = kwargs.get('tag')
        plat = '{}/{}'.format(kwargs.get('os'), kwargs.get('arch'))
        image = self.client.images.get(f'{repo}:{tag}')
        if image is None:
            print(f'Error: Image {repo}:{tag} not found')
            return
        print(f'Pushing {repo}:{tag}, platform={plat}')
        push_stream = self.client.api.push(repo, tag=tag, stream=True, decode=True)
        push_layers = {}
        pbar = None
        for output in push_stream:
            if not isinstance(id := output.get('id'), str) or id == tag:
                continue
            push_layers.setdefault(id, {})
            if isinstance(detail := output.get('progressDetail'), dict):
                push_layers[id].update(detail)
            if isinstance(status := output.get('status'), str):
                push_layers[id].update({'status': status})
            complete = sum([1 for v in push_layers.values() if v.get('status') in ['Layer already exists', 'Pushed']])
            current = sum([s for v in push_layers.values() if isinstance(s := v.get('current'), int)])
            total = sum([s for v in push_layers.values() if isinstance(s := v.get('total'), int)])
            if total == 0:
                continue
            if pbar is None:
                pbar = tqdm(total=total, unit='B', unit_scale=True, desc='  Pushing', dynamic_ncols=True)
            else:
                pbar.total = total
            pbar.desc = f'  Pushing {complete}/{len(push_layers)} layers'
            pbar.n = current
            pbar.refresh()
        pbar and pbar.close()
        kwargs.get('debug') and print(push_layers)
        print(f'  Digest: {image.id}')

    def rmi(self, **kwargs):
        repo = kwargs.get('repo')
        tag = kwargs.get('tag')
        plat = '{}/{}'.format(kwargs.get('os'), kwargs.get('arch'))
        kwargs.get('debug') in [True, None] and print(f'Removing {repo}:{tag}, platform={plat}')
        self.client.images.remove(f'{repo}:{tag}')

    def prune(self, force=False):
        if force:
            print('Pruning stopped containers and orphan images')
            self.client.containers.prune()
        else:
            print('Pruning orphan images')
        self.client.images.prune(filters={'dangling': True})
        for image in self.client.images.list():
            if len(image.tags) > 0:
                continue
            try:
                print('Removing {}'.format(image.id.removeprefix('sha256:')))
                self.client.images.remove(image.id)
            except (APIError, HTTPError):
                print('  Failed: Image {} is being used'.format(image.short_id.removeprefix('sha256:')))


def _config(args):
    config = Config()
    config.debug() and print(args)
    if args.subcommand == 'ls':
        for key, value in config.data.items():
            print(f'{key}: {value}')
    elif args.subcommand == 'get':
        print(f'{args.key}:', config.get(args.key))
    elif args.subcommand == 'set':
        config.set(args.key, args.value)
        config.save()
    elif args.subcommand == 'unset':
        config.data.pop(args.key, None)
        config.save()
    elif args.subcommand == 'add':
        if isinstance(config.data[args.key], list):
            config.data[args.key].append(args.value)
        else:
            config.data[args.key] = [args.value]
        config.save()
    elif args.subcommand == 'del':
        if isinstance(config.data[args.key], list):
            config.data[args.key].remove(args.value)
        else:
            config.data.pop(args.key, None)
        config.save()
    else:
        print(f'Invalid subcommand: {args.subcommand}')


def _fetch(args):
    config = Config()
    config.debug() and print(args)
    pattern = args.pattern
    try:
        docker = Docker()
        cache = Cache()
        images = cache.sort(docker.images())
        config.debug() and print(images)
        for image in images:
            name = '{}:{}'.format(image.get('repo'), image.get('tag'))
            if isinstance(config.registry, str) and name.startswith(config.registry + '/'):
                docker.rmi(**image)
                continue
            if isinstance(pattern, str) and re.search(pattern, name) is None:
                continue
            if not image.get('exist', True):
                config.debug() and print(f'Skipped: Image {name} not exist')
                continue
            for i in range(1, config.retry + 1):
                try:
                    info = docker.pull(**{**image, 'debug': config.debug()})
                    cache.set(**{**info, 'exist': True})
                    break
                except ImageNotFound:
                    cache.set(**{**image, 'exist': False})
                    print('  Failed: Image not found')
                    config.debug() and print(image)
                    break
                except (APIError, HTTPError):
                    config.debug() and traceback.print_exc()
                    print('  Error: Failed to connect to Docker API' + (', retrying' if i < config.retry else ''))
                    time.sleep(1.5)
    except KeyboardInterrupt:
        pass
    except DockerException:
        config.debug() and traceback.print_exc()
        print('Error: Docker is not installed or not running')
    except Exception:
        config.debug() and traceback.print_exc()


def _sync(args):
    config = Config()
    config.debug() and print(args)
    pattern = args.pattern
    registry = args.registry or config.registry
    if not isinstance(registry, str):
        print('Error: Registry not specified')
        return
    try:
        docker = Docker()
        cache = Cache()
        for image in docker.images():
            name = '{}:{}'.format(image.get('repo'), image.get('tag'))
            if isinstance(registry, str) and name.startswith(registry + '/'):
                try:
                    docker.rmi(**image)
                except ImageNotFound:
                    pass
                continue
            if isinstance(pattern, str) and re.search(pattern, name) is None:
                continue
            hist = cache.get(**image)
            if hist and isinstance(r := hist.get('registry'), dict) and r.get(registry) == image.get('id'):
                config.debug() and print(f'Skipped: Image {name} already synced')
                continue
            secs = [x for x in image.get('repo').split('/') if len(x)]
            if len(secs) == 0:
                print(f'Error: Invalid repository name: {name}')
                continue
            if len(secs) > 2:
                secs = secs[-2:]
            elif len(secs) == 1:
                secs.insert(0, 'library')
            if len(secs) != 2:
                print(f'Error: Invalid repository name processing: {secs}')
                continue
            secs.insert(0, registry)
            mirror = {
                'repo': '/'.join(secs),
                'tag': image.get('tag'),
                'os': image.get('os'),
                'arch': image.get('arch'),
                'debug': config.debug(),
            }
            for i in range(1, config.retry + 1):
                try:
                    docker.tag(name, **mirror)
                    docker.push(**mirror)
                    docker.rmi(**mirror)
                    hist = hist or {}
                    hist.update(image)
                    hist.setdefault('registry', {}).update({registry: image.get('id')})
                    cache.set(**hist)
                    break
                except ImageNotFound:
                    print(f'  Failed: Image not found: {image}')
                    break
                except (APIError, HTTPError):
                    config.debug() and traceback.print_exc()
                    print('  Error: Failed to connect to Docker API' + (', retrying' if i < config.retry else ''))
                    time.sleep(1.5)
    except KeyboardInterrupt:
        pass
    except DockerException:
        config.debug() and traceback.print_exc()
        print('Error: Docker is not installed or not running')
    except Exception:
        config.debug() and traceback.print_exc()


def _prune(args):
    config = Config()
    config.debug() and print(args)
    try:
        docker = Docker()
        docker.prune(args.force)
    except KeyboardInterrupt:
        pass
    except DockerException:
        config.debug() and traceback.print_exc()
        print('Error: Docker is not installed or not running')
    except Exception:
        config.debug() and traceback.print_exc()


def main():
    args = _parser().parse_args()
    if args.command == 'config':
        _config(args)
    elif args.command == 'fetch':
        _fetch(args)
    elif args.command == 'sync':
        _sync(args)
    elif args.command == 'prune':
        _prune(args)
    else:
        _parser().print_help()


if __name__ == '__main__':
    main()
