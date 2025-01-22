from re import compile

from setux.core.module import Module
from setux.logger import debug


class Distro(Module):
    '''Update Config File (sed)
    '''

    def deploy(self, target, *, path, line, select=None, sudo=None, user=None, group=None, mode=None):
        cont = self.target.read(path, sudo=sudo, report='quiet')
        msg = [f'{path} <>']
        modified = False
        if select:
            sre = compile(select).search
            updated, found = [], False
            for cur in cont.split('\n'):
                if sre(cur):
                    found = True
                    if cur == line:
                        updated.append(cur)
                    else:
                        msg.append(f' <  {cur}')
                        msg.append(f'  > {line}')
                        updated.append(line)
                        modified = True
                else:
                    updated.append(cur)
            if not found:
                updated.append(line)
                modified = True
            if modified:
                target.write(path, '\n'.join(updated)+'\n', sudo=sudo, report='quiet')
        else:
            modified = True
            msg.append(f'  > {line}')
            target.write(path, f'{cont}{line}\n', sudo=sudo, report='quiet')

        debug('\n'.join(msg))
        return modified
