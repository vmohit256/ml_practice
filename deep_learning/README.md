
# Notes

- types of models
    - actual biological neurons  TODO: read up on everything known about biological neurons, their structure, function, etc.
        - are they binary? or do they fire at different rates?
        - "Cells that fire together, wire together." // what does this mean exactly?
        - sigmoid activation function seems to model biological neurons well
    - artificial neuron
        - a neuron as N binary inputs and a binary output
        - output = 1 if sum(inputs) >= threshold else 0
        - inhibition: an inhibit input can inhibit the neuron from firing no matter what the other inputs are active
        - can represent any propositional logic function
    - perceptron
        - h_w(x) = step(w^T * x) (aka threshold logic unit)
    - multi-layer perceptron
        - replace step function with sigmoid function to allow for gradient descent in back propagation
        - if weights are initialized to 0, then due to symmetry, all neurons in a layer will have the same weights, gradients, etc. and will learn the same thing. To break symmetry, weights are initialized randomly.
        - activation functions are needed to introduce non-linearity into the model
- loss functions
    - huber loss for regression
        - L(y, y_pred) = 1/2 * (y - y_pred)^2 if |y - y_pred| <= delta else delta * |y - y_pred| - 1/2 * delta^2. delta = 1 for example
            - less sensitive to outliers than mean squared error and converges faster

# References

- [Hands-On ML](https://github.com/ageron/handson-ml3)
- [Standford CS230](https://cs230.stanford.edu/syllabus/)
    - [Past projects](https://cs230.stanford.edu/past-projects/)