from imageai.Prediction.Custom import ModelTraining

data_dir = ""
train_model_args = dict(num_objects=75,
                        num_experiments=100,
                        enhance_data=True,
                        batch_size=32,
                        show_network_summary=True)

model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()
model_trainer.setDataDirectory(data_dir)
model_trainer.trainModel(**train_model_args)
