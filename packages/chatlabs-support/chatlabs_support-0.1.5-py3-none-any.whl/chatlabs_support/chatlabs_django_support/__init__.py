from importlib.util import find_spec

from ..exceptions import ModuleDependenciesError

if not find_spec("django"):
    raise ModuleDependenciesError(
        current_module='chatlabs_django_support',
        required_module='chatlabs-support[chatlabs_django_support]',
    )
