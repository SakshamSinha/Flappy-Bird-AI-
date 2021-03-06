"""
Neural network using Keras (called by q_net_keras)
.. Author: Vincent Francois-Lavet
"""

import numpy as np
from keras.models import Model
from keras.layers import Input, Layer, Dense, Flatten, merge, Activation, Conv2D, MaxPooling2D, Reshape, Permute

class NN():
    """
    Deep Q-learning network using Keras

    Parameters
    -----------
    batch_size : int
        Number of tuples taken into account for each iteration of gradient descent
    input_dimensions :
    n_actions :
    random_state : numpy random number generator
    action_as_input : Boolean
        Whether the action is given as input or as output
    """
    def __init__(self, batch_size, input_dimensions, n_actions, random_state,
                 action_as_input=False):
        self._input_dimensions=input_dimensions
        self._batch_size=batch_size
        self._random_state=random_state
        self._n_actions=n_actions

    def _buildDQN(self):
        """
        Build a network consistent with each type of inputs
        """
        layers=[]
        outs_conv=[]
        inputs=[]

        for i, dim in enumerate(self._input_dimensions):
            # - observation[i] is a FRAME
            assert len(dim) == 3
            input = Input(shape=(dim[0],dim[1],dim[2]))
            inputs.append(input)
            reshaped=Permute((2,3,1), input_shape=(dim[0],dim[1],dim[2]))(input)    #data_format='channels_last'
            x = Conv2D(8, (4, 4), strides=2, activation='relu', padding='valid')(reshaped)   #Conv on the frames
            x = Conv2D(16, (3, 3), activation='relu', padding='valid')(x)         #Conv on the frames
            x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid')(x)
            x = Conv2D(16, (3, 3), activation='relu', padding='valid')(x)         #Conv on the frames
            x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid')(x)

            out = Flatten()(x)

            outs_conv.append(out)

        if len(outs_conv)>1:
            x = merge(outs_conv, mode='concat')
        else:
            x = outs_conv [0]

        # we stack a deep fully-connected network on top
        x = Dense(50, activation='relu')(x)
        x = Dense(20, activation='relu')(x)

        if ( isinstance(self._n_actions,int)):
            out = Dense(self._n_actions)(x)
        else:
            out = Dense(len(self._n_actions))(x)

        model = Model(input=inputs, output=out)
        layers=model.layers

        # Grab all the parameters together.
        params = [ param
                    for layer in layers
                    for param in layer.trainable_weights ]

        return model, params

if __name__ == '__main__':
    pass

