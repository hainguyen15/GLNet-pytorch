from distutils.command.build_ext import build_ext as DistUtilsBuildExt
import setuptools
# from setuptools.extension import Extension

class BuildExtension(setuptools.Command):
    description     = DistUtilsBuildExt.description
    user_options    = DistUtilsBuildExt.user_options
    boolean_options = DistUtilsBuildExt.boolean_options
    help_options    = DistUtilsBuildExt.help_options

    def __init__(self, *args, **kwargs):
        from setuptools.command.build_ext import build_ext as SetupToolsBuildExt

        # Bypass __setatrr__ to avoid infinite recursion.
        self.__dict__['_command'] = SetupToolsBuildExt(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._command, name)

    def __setattr__(self, name, value):
        setattr(self._command, name, value)

    def initialize_options(self, *args, **kwargs):
        return self._command.initialize_options(*args, **kwargs)

    def finalize_options(self, *args, **kwargs):
        ret = self._command.finalize_options(*args, **kwargs)
        import numpy
        self.include_dirs.append(numpy.get_include())
        return ret

    def run(self, *args, **kwargs):
        return self._command.run(*args, **kwargs)

setuptools.setup(
    name             = 'GLNet',
    version          = '0.1.0',
    description      = 'Pytorch implementation of GLNet Semantic Segmentation.',
    url              = 'https://github.com/hainguyen15/GLNet-pytorch',
    author           = 'Hai Nguyen',
    author_email     = 'quanghai.ng1512@gmail.com',
    maintainer       = 'Hai Nguyen',
    maintainer_email = 'quanghai.ng1512@gmail.com',
    cmdclass         = {'build_ext': BuildExtension},
    packages         = setuptools.find_packages(),
    install_requires = ['pytorch', 'opencv-python', 'tqdm'],
    entry_points     = {
        'console_scripts': [
            'retinanet-train=keras_retinanet.bin.train:main',
            'retinanet-evaluate=keras_retinanet.bin.evaluate:main',
            'retinanet-debug=keras_retinanet.bin.debug:main',
            'retinanet-convert-model=keras_retinanet.bin.convert_model:main',
        ],
    },
    # ext_modules    = extensions,
    setup_requires = ["numpy>=1.14.0"]
)
