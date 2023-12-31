
import CMAPSS_Dataloader
import CMAPSS_CNN
import CMAPSS_TrainLoop
import CMAPSS_PlotFunctions
import CMPASS_Clustering

sub_dataset="001"
window_size=30
max_life=125
scaler="mm"
scaler_range=(-1,1)
shuffle=True
batch_size=512
algorithm = "CNN"
num_epochs = 2
alpha_grid=0.4
alpha_low=0.6
alpha_high=0.9
_COLORS=["green", "teal"]
read_path = r"..\Datasets\CMAPSSData/"

'''
CMPASS_Clustering.cluster takes raw data set as input. Perfomes clustering by operating settings
and give dataframe with an additional column named operating_condition as output
'''
train_data, test_data = CMPASS_Clustering.cluster(read_path, sub_dataset)

'''
CMPASS_Clustering.oc_history_cols takes dataframe generated by CMPASS_Clustering.cluster as input,
calculated history of operating conditions and if save=True then gives a .csv file of original data
plus 6 cols of history
'''
CMPASS_Clustering.oc_history_cols(read_path, sub_dataset, train_data, test_data, save=True)

'''
CMAPSS_Dataloader take .csv files as input and prepare data s that it can be fed to CNN model
The shape of output data will be [Batch_size, Channels, Sequence_length, Sensors]
'''
_,_,train_loader, test_loader, unshuffle_train_loader, finaltest_loader=CMAPSS_Dataloader.LoadCMAPSS(read_path, sub_dataset,
                                                                                   window_size, max_life, scaler, 
                                                                                   scaler_range, shuffle,
                                                                                   batch_size, cluster=True)
'''
CMAPSS_CNN.Network prepared CNN model
'''
model, optimizer, loss_func = CMAPSS_CNN.Network(algorithm = "CNN")

'''
CMAPSS_TrainLoop.Train Train, Validate and Tests the model
'''
train_loss_epoch, test_loss_epoch, train_output, test_output, finaltest_output = CMAPSS_TrainLoop.Train(train_loader, test_loader, 
                                                                                       unshuffle_train_loader,
                                                                                       finaltest_loader, 
                                                                                       model, optimizer, 
                                                                                       loss_func, 
                                                                                       num_epochs)

'''
CMAPSS_PlotFunctions.train_actual_predicted taked input from CMAPSS_TrainLoop.Train and
plots the actual RUL vs. Predicted RUL for train data
'''
CMAPSS_PlotFunctions.train_actual_predicted(read_path, sub_dataset, window_size, max_life, train_output, alpha_grid, alpha_low, alpha_high, _COLORS)

'''
CMAPSS_PlotFunctions.test_actual_predicted taked input from CMAPSS_TrainLoop.Train and
plots the actual RUL vs. Predicted RUL for test data
'''
CMAPSS_PlotFunctions.test_actual_predicted(read_path, sub_dataset, window_size, max_life, test_output, alpha_grid, alpha_low, alpha_high, _COLORS)

'''
CMAPSS_PlotFunctions.loss_plot taked input from CMAPSS_TrainLoop.Train and
plots the train and test loss
'''
CMAPSS_PlotFunctions.loss_plot(sub_dataset, train_loss_epoch, test_loss_epoch, alpha_grid, alpha_low, alpha_high, _COLORS)

'''
CMAPSS_PlotFunctions.fianltest_actual_vs_predicted taked input from CMAPSS_TrainLoop.Train and
plots the actual RUL vs. Predicted RUL for finaltest dataand also gives the final score
'''
socre = CMAPSS_PlotFunctions.fianltest_actual_vs_predicted(read_path, sub_dataset, window_size, max_life, finaltest_output, alpha_grid, 
                                                           alpha_low, alpha_high, _COLORS)


