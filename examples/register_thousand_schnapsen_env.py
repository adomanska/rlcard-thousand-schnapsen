from rlcard_thousand_schnapsen.envs import make

if __name__ == "__main__":
    env = make('thousand-schnapsen', config={'seed': 0})
