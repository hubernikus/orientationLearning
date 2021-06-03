#!/usr/bin/python3
"""
Directional [SEDS] Learning
"""
__author__ =  "lukashuber"
__date__ = "2021-05-16"

import os

import matplotlib.pyplot as plt

# from motion_learning_direction_space.learner.directional import DirectionalGMM
from motion_learning_direction_space.learner.directional_gmm import DirectionalGMM


if (__name__) == "__main__":
    plt.close('all')
    plt.ion() # continue program when showing figures
    save_figure = False
    showing_figures = True

    name = None
    # plt.close("all")
    print("Start script .... \n")

    name = "2D_messy-snake"
    n_gaussian = 17

    # name = "2D_incremental_1"
    # n_gaussian = 5

    # dataset_name = "dataset/2D_Sshape.mat"
    # n_gaussian = 5

    # dataset_name = "dataset/2D_Ashape.mat"
    # n_Gaussian = 6
    n_samples = None
    attractor = None

    if False:
        dataset_name = "dataset/2D_messy-snake.mat"
        n_gaussian = 17

    elif False:
        dataset_name = "dataset/2D_incremental_1.mat"
        n_gaussian = 5

    elif False:
        dataset_name = "dataset/2D_Sshape.mat"
        n_gaussian = 5
        # n_samples = 300
        attractor = [-4.3, 0]

    elif True:
        name = "2D_Ashape"
        n_gaussian = 6
        # n_samples = 100
        
    elif False:
        name = "2D_multi-behavior"
        n_gaussian = 11
    
    elif False:
        dataset_name = "dataset/3D_Cshape_top.mat"

    if name is not None:
        dataset_name = os.path.join("dataset", name+".mat")

    MainLearner = DirectionalGMM()
    MainLearner.load_data_from_mat(file_name=dataset_name)
    MainLearner.regress(n_gaussian=n_gaussian)

    gauss_colors = MainLearner.complementary_color_picker(n_colors=n_gaussian)

    # Visualization
    # MainLearner.plot_gaussians_all_directions()
    
    MainLearner.plot_position_and_gaussians_2d(colors=gauss_colors)
    if save_figure:
        plt.savefig(os.path.join("figures", name+"_gaussian_and_2d"+".png"), bbox_inches="tight")
                    
    MainLearner.plot_vectorfield_and_integration()
    # MainLearner.plot_vectorfield_and_data()
    if save_figure:
        plt.savefig(os.path.join("figures", name+"_vectorfield"+".png"), bbox_inches="tight")
        
    # MainLearner.plot_time_direction_and_gaussians()
    # MainLearner.plot_vector_field_weights(n_grid=100, colorlist=gauss_colors, pos_vel_input=True)
    # MainLearner.plot_vector_field_weights(n_grid=100, colorlist=gauss_colors)
    if save_figure:
        plt.savefig(os.path.join("figures", name+"weights"+".png"), bbox_inches="tight")
    

    plt.show()
    
print("\n\n\n... script finished.")
