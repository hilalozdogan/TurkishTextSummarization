
class PagerankClass():

    def calculate_page_rank(self,graph, d, n_iter):
        n_sent = len(graph)
        if n_sent > 0:
            jump_random = d / n_sent
            prob_not_dumping = 1 - d
            PR = dict.fromkeys(graph.keys(), 1 / n_sent)
            for i in range(n_iter):
                PR_new = {}
                for node in graph:
                    sum_links = 0
                    for link in graph[node]:
                        sum_links += PR[link] / len(graph[link])
                    PR_new[node] = jump_random + (prob_not_dumping * sum_links)
                PR = PR_new
            return PR
        return {}

