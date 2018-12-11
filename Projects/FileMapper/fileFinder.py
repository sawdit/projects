from fs.osfs import OSFS

home_fs = OSFS("/")

home_fs.listdir('/')

fs_tree = home_fs.tree