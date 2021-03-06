#!/usr/bin/python3
"""
Directional [SEDS] Learning
"""
# Author: Lukas Huber
# Email: hubernikus@gmail.com
# License: BSD (c) 2021
import os

import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec

from vartools.dynamical_systems import LinearSystem

from dynamic_obstacle_avoidance.avoidance import obstacle_avoidance_rotational
from dynamic_obstacle_avoidance.visualization import Simulation_vectorFields, plot_obstacles
from dynamic_obstacle_avoidance.visualization.gamma_field_visualization import gamma_field_multihull

# from motion_learning_direction_space.learner.directional import DirectionalGMM
from motion_learning_direction_space.learner.directional_gmm import DirectionalGMM
from motion_learning_direction_space.graph import GraphGMM
# motion_learning_direction_space/visualization/
from motion_learning_direction_space.visualization.convergence_direction import test_convergence_direction_multihull


if (__name__) == "__main__":
    # plt.close('all')
    plt.ion() # continue program when showing figures
    save_figure = True
    showing_figures = True
    name = None
    
    print("Start script .... \n")

    if True:
        name = "2D_Ashape"
        n_gaussian = 6

    if name is not None:
        dataset_name = os.path.join("dataset", name+".mat")

    if True: # relearn (debugging only)
        import numpy as np
        np.random.seed(4)
        MainLearner = GraphGMM(file_name=dataset_name, n_gaussian=n_gaussian)
        # MainLearner = DirectionalGMM()
        # MainLearner.load_data_from_mat(file_name=dataset_name)
        # MainLearner.regress(n_gaussian=n_gaussian)
        # gauss_colors = MainLearner.complementary_color_picker(n_colors=n_gaussian)

    # MainLearner.plot_position_data()
    # MainLearner.plot_position_and_gaussians_2d(colors=gauss_colors)
    MainLearner.create_learned_boundary()

    # Is now included in learned boundary.
    # MainLearner.create_graph_from_gaussians() 

    
    if False:
        MainLearner.plot_obstacle_wall_environment()
        # plt.savefig(os.path.join("figures", name+"_convergence_direction" + ".png"), bbox_inches="tight")
    
    # pos_attractor = MainLearner.pos_attractor
    
    MainLearner.set_convergence_directions(NonlinearDynamcis=MainLearner)
    
    x_lim, y_lim = MainLearner.get_xy_lim_plot()

    plot_gamma_value = False
    if plot_gamma_value:
        n_subplots = 6
        n_cols = 3
        n_rows = int(n_subplots / n_cols)
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, 10))

        for it_obs in range(n_subplots):
            it_x = it_obs % n_rows
            it_y = int(it_obs / n_rows)
            ax = axs[it_x, it_y]
            
            gamma_field_multihull(MainLearner, it_obs,
                                  n_resolution=100, x_lim=x_lim, y_lim=y_lim, ax=ax)

        plt.subplots_adjust(wspace=0.001, hspace=0.001)
        if save_figure:
            plt.savefig(os.path.join("figures", "gamma_value_subplots" + ".png"),
                        bbox_inches="tight")

    plot_local_attractor = True
    if plot_local_attractor:
        n_subplots = 6
        n_cols = 3
        n_rows = int(n_subplots / n_cols)
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, 10))

        for it_obs in range(n_subplots):
        # for it_obs in [1]:
            it_x = it_obs % n_rows
            it_y = int(it_obs / n_rows)
            ax = axs[it_x, it_y]

            # fig, ax = plt.subplots(1, 1, figsize=(15, 10))
            
            test_convergence_direction_multihull(
                MainLearner, it_obs, n_resolution=30, x_lim=x_lim, y_lim=y_lim, ax=ax,
                assert_check=False)
            
        plt.subplots_adjust(wspace=0.001, hspace=0.001)
        # if save_figure:
        if True:
            plt.savefig(os.path.join("figures", "test_convergence_direction" + ".png"),
                        bbox_inches="tight")
        
    plot_vectorfield = True
    if plot_vectorfield:
        n_resolution = 30
        
        # def initial_ds(position):
            # return evaluate_linear_dynamical_system(position, center_position=pos_attractor)

        InitialSystem = LinearSystem(attractor_position=MainLearner.attractor_position)
            
        # fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        Simulation_vectorFields(
            x_lim, y_lim, n_resolution,
            # obs=obstacle_list,
            # point_grid=3,
            obs=MainLearner,
            saveFigure=True,
            figName=name+"_converging_linear_base",
            noTicks=True, showLabel=False,
            draw_vectorField=True,
            dynamical_system=InitialSystem.evaluate,
            obs_avoidance_func=obstacle_avoidance_rotational,
            automatic_reference_point=False,
            pos_attractor=InitialSystem.attractor_position,
            fig_and_ax_handle=(fig, ax),
            # Quiver or Streamplot
            show_streamplot=False,
            # show_streamplot=False,       
            )


    # if True:
        # MainLearner.set_convergence_directions(NonlinearDynamcis=MainLearner)
        MainLearner.reset_relative_references()

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        Simulation_vectorFields(
            x_lim, y_lim, n_resolution,
            # obs=obstacle_list,
            obs=MainLearner,
            saveFigure=True,
            figName=name+"_converging_nonlinear_base",
            noTicks=True, showLabel=False,
            draw_vectorField=True,
            dynamical_system=MainLearner.predict,
            obs_avoidance_func=obstacle_avoidance_rotational,
            automatic_reference_point=False,
            pos_attractor=MainLearner.attractor_position,
            fig_and_ax_handle=(fig, ax),
            # Quiver or Streamplot
            show_streamplot=False,
            # show_streamplot=False,       
            )
        MainLearner.reset_relative_references()

        # plt.savefig(os.path.join("figures", name+"_converging_linear_base" + ".png"), bbox_inches="tight")
    plt.show()
    
print("\n\n\n... script finished.")
