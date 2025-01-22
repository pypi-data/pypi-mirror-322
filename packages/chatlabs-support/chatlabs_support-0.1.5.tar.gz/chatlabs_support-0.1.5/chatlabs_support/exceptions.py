class ModuleDependenciesError(ImportError):
    def __init__(self, current_module: str, required_module: str):
        super().__init__(
            f'To use the {current_module} module, install the library '
            f'with `{required_module}`.'
        )
