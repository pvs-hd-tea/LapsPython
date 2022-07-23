"""One-click demo."""

if __name__ == '__main__':
    import random

    from lapspython.pipeline import Pipeline

    random.seed(3)
    Pipeline.from_checkpoint('re2_best_dsl_language')
    print(f'\n{"="*79}\n')
    Pipeline.from_checkpoint('re2_test', mode='R')
