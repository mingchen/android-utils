#
# Copyright (c) 2012, Ming Chen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: Ming Chen
# Date: 2012-8-10
#
import os
import sys
import shutil # file operation utilities

#
# those packages will not copy to destination directory.
#
filtered_packages = ('test', 'test2', 'sample', 'doclava',
                     'javassist', 'java_cup', 'name', 'jdiff',
                     'signature', 'vogar');

def get_package_path(file_path):
  """
    Get a java file's package name.

    example of return 'com/example'
    if no package delcaraion is found, return ''
  """
  package_path = '';
  f = file(file_path, 'r');
  while True:
    line = f.readline();
    if len(line) == 0:  # zero length indicates EOF
      break;
    pos = line.find('package ');
    #
    # 'package' keyword should at the beginning of a line
    #
    if pos == 0:
      # found
      package = line[pos+len('package '):];
      package = package.strip(' \r\n\t;');

      # package may include comments, e.g.
      #
      # java/util; // android-changed: com/ibm/icu/impl (ICU4J 4/2)
      #
      pos = package.find(';');
      if pos != -1:
        package = package[0:pos];
      package_path = package.replace('.', '/');
      break;
  f.close();
  return package_path;

def walk_source_tree(path, target_dir):
  """
  walk through the Android source tree and copy the .java file to target_dir.
  """
  old_package_path = '';
  for dir, subdirs, files in os.walk(path):
    for file in files:
      #
      # Only process .java file
      # and path do not include tests, this will filter test files.
      #
      if file.endswith('.java') and dir.find('tests') == -1:
        full_path = os.path.join(dir, file);
        package_path = get_package_path(full_path);

        if package_path == '':
          continue;

        if package_path.startswith(filtered_packages):
          continue;
        
        package_path = target_dir + '/' + package_path;
        if package_path != old_package_path:
          # create package path if not exist.
          if not os.path.exists(package_path):
            os.makedirs(package_path)
          old_package_path = package_path
        dst_file = "%s/%s" % (package_path, file)
        shutil.copyfile(full_path, dst_file)

      
def main(argv):
  """
  Usage: extact_android_sdk_src.py <android src directory> <output directory>
  """
  if len(argv) != 3:
    print "Extract Android Java source code"    
    print "Usage: %s <android src directory> <output directory>" % argv[0]
    print "  <android src directory>  Android source tree directory"
    print "  <output directory>       Output directory for java source code"
    print "Example: %s android-4.0.1_r1 D:/android-4.0.1-sdk-src" % argv[0]    
    exit(1);
    
  walk_source_tree(argv[1], argv[2]);

if __name__ == '__main__':
  main(sys.argv);
