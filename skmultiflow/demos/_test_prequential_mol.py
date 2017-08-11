__author__ = 'Guilherme Matsumoto'

from sklearn.linear_model.stochastic_gradient import SGDClassifier, SGDRegressor
from sklearn.linear_model.passive_aggressive import PassiveAggressiveClassifier
from sklearn.linear_model.perceptron import Perceptron
from skmultiflow.classification.perceptron import PerceptronMask
from skmultiflow.classification.multi_output_learner import MultiOutputLearner
from skmultiflow.core.pipeline import Pipeline
from skmultiflow.data.file_stream import FileStream
from skmultiflow.options.file_option import FileOption
from skmultiflow.data.generators.multilabel_generator import MultilabelGenerator
from skmultiflow.data.generators.waveform_generator import WaveformGenerator
from skmultiflow.evaluation.evaluate_prequential import EvaluatePrequential


def demo(output_file=None, instances=40000):
    # Setup the File Stream
    #opt = FileOption("FILE", "OPT_NAME", "../datasets/music.csv", "CSV", False)
    #stream = FileStream(opt, 0, 6)
    stream = MultilabelGenerator(n_samples=instances)
    #stream = WaveformGenerator()
    stream.prepare_for_use()


    # Setup the classifier
    classifier = MultiOutputLearner(SGDClassifier(n_iter=100))
    #classifier = SGDClassifier()
    #classifier = PassiveAggressiveClassifier()
    #classifier = SGDRegressor()
    #classifier = PerceptronMask()

    # Setup the pipeline
    pipe = Pipeline([('Classifier', classifier)])

    # Setup the evaluator
    eval = EvaluatePrequential(pretrain_size=5000, max_instances=instances-10000, batch_size=1, n_wait=200, max_time=1000,
                               output_file=output_file, task_type='multi_output', show_plot=True, plot_options=['hamming_score', 'j_index', 'exact_match'])

    # Evaluate
    eval.eval(stream=stream, classifier=pipe)

if __name__ == '__main__':
    demo('log_mol1.csv', 50000)