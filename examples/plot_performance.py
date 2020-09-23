import click
import csv
import matplotlib.pyplot as plt
from typing import Optional

plt.style.use('ggplot')


@click.command()
@click.option('--path',
              type=click.Path(exists=True),
              required=True,
              help='Path to csv')
@click.option('--count', type=click.INT, help='Iterations count')
def run(path: str, count: Optional[int]):
    with open(path) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        rewards = [int(reward) for _, reward in data]
        if count is not None:
            rewards = rewards[0:count]
        plt.plot(rewards)
        plt.xlabel('Iteration')
        plt.ylabel('Reward')
        plt.show()


if __name__ == '__main__':
    run()
