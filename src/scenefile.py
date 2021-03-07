class SceneFile(object):
    def __init__(self, folder_path, descriptor, task, version, ext):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.version = version
        self.ext = ext

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.version,
                              ext=self.ext)


scene_file = SceneFile("C:\\", "tank", "model", 1, ".ma")
print(scene_file.filename)
