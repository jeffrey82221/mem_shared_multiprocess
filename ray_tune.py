import ray
from ray import tune
from ray.tune import register_trainable

def f(config):
    x = config['x']
    return x

register_trainable("f", f)
ray.init(num_cpus=16, num_gpus=0)

analysis = tune.run(
    f,
    name="f",
    stop={
        "training_iteration": 3,
    },
    num_samples=30,
    max_failures=5,
    config={
        "x": tune.grid_search([0, 1, 2, 3, 4])},
    resources_per_trial={
        "cpu": 1,
        "gpu": 0,
        "extra_gpu":0
    }
)

print("Best trail is", analysis.get_best_trial(metric="x", mode='max', scope='all'))
