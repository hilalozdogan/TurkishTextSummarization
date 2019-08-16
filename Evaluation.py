import rouge


def prepare_results(m, p, r, f):
    return '\t{}:\t{}: {:5.2f}\t{}: {:5.2f}\t{}: {:5.2f}'.format(m, 'P', 100.0 * p, 'R', 100.0 * r, 'F1', 100.0 * f)


for aggregator in ['Avg']:
    print('Evaluation with {}'.format(aggregator))
    apply_avg = aggregator == 'Avg'


    evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l', 'rouge-w'],
                           max_n=4,
                           limit_length=True,
                           length_limit=100,
                           length_limit_type='words',
                           apply_avg=apply_avg,
                           #apply_best=apply_best,
                           alpha=0.5, # Default F1_score
                           weight_factor=1.2,
                           stemming=True)
    hypothesis=[ ]
    hypothesisML =[ ]
    references=[ ]
    for x in range(1, 4):
        sentenceList = ''
        sentenceListSum = ''
        fileNameSummary = 'Veriseti/Summary' + str(x) + ".txt"
        fileNameGenerated = 'Veriseti/GeneratedSummary' + str(x) + ".txt"
        openSummary = open(fileNameSummary, "r")
        readSummary = openSummary.read()
        openGeneratedSummary = open(fileNameGenerated, "r")
        readGeneratedSummary = openGeneratedSummary.read()
        hypothesis.append(readGeneratedSummary)
        references.append(readSummary)


    all_hypothesis = [hypothesis[0], hypothesis[1],hypothesis[2]]
    all_references = [references[0], references[1], references[2]]

    scores = evaluator.get_scores(all_hypothesis, all_references)

    for metric, results in sorted(scores.items(), key=lambda x: x[0]):
        if not apply_avg:
            for hypothesis_id, results_per_ref in enumerate(results):
                nb_references = len(results_per_ref['p'])
            print()
        else:
            print(prepare_results(metric, results['p'], results['r'], results['f']))
    print()


