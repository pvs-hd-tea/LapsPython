"""One-click demo."""

if __name__ == '__main__':
    from lapspython.pipeline import Pipeline

    Pipeline.from_checkpoint('re2_best_dsl_language')
    print('\n-------------------------------------------------------------\n')
    Pipeline.from_checkpoint('re2_test', mode='R')
