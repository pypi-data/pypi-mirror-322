from setuptools import setup, find_packages
from setuptools.command.bdist_wheel import bdist_wheel, safer_name, safer_version
import os
import shutil
from .. import natten_installer as ni
from .. import pypi


class Setup:
    def make_install_requires(self, version):
        self.executable = ni.parent_python()
        command, self.combined_version, self.wheel_filename = ni.make_natten_package_command(version, self.executable, True, True, True)
        return command
    
    @classmethod
    def make_dist_info(cls, name, version):
        name = safer_name(name)
        version = safer_version(version)
        distinfo_dirname = f'{name}-{version}.dist-info'
        return distinfo_dirname
    
    def post_build_dist_wheel(self, bdw: bdist_wheel):
        impl_tag, abi_tag, plat_tag = bdw.get_tag()
        archive_basename = f"{bdw.wheel_dist_name}-{impl_tag}-{abi_tag}-{plat_tag}"
        wheel_path = os.path.join(bdw.dist_dir, archive_basename + ".whl")
        os.remove(wheel_path)
        natten_wheel_path = os.path.join(pypi.download_temp_dir, self.wheel_filename)
        shutil.move(natten_wheel_path, wheel_path)
        os.symlink(os.path.abspath(wheel_path), os.path.abspath(natten_wheel_path))

    @classmethod
    def run(cls, name, version):
        instance = cls()
        
        
        class PostBuildDistWheel(bdist_wheel):
            def run(self):
                super().run()
                instance.post_build_dist_wheel(self)


        setup(
            name=name.strip('fit-'),
            version=version,
            install_requires=instance.make_install_requires(version),
            packages=find_packages(),
            cmdclass={
                'bdist_wheel': PostBuildDistWheel,
            },
        )