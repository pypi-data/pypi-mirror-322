import segment_annotation_manager as sam

config = sam.Config(file=r'C:\Users\Alexander\PycharmProjects\Segment_Annotation_Manager\tests\configs\test.yaml')
annotation = sam.Annotation()
config.update(annotation, stage='train')
