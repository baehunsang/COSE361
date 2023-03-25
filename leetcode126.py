import collections
class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList):
        if endWord not in wordList:
            return []
        word_dict = collections.defaultdict(list)
        result = []
        #Initilize word_dict
        for word in wordList:
            for i in range(len(word)):
                word_dict[word[:i]+"*"+word[i+1:]].append(word)
        
        #Initialize visited and Queue
        Q_forward = collections.deque([beginWord])
        Q_backword = collections.deque([endWord])

        #key-> node, value-> parent node
        #Path generator are needed
        visited_forward = {beginWord: []}
        visited_backward = {endWord: []}

        #Proceed in Bidirectional search
        def Proceed(Q, visited1, visited2, is_forward):
            #Level dict to avoide collision in making path
            level_dict = collections.defaultdict(list)
            #Expand one level of graph
            for _ in range(len(Q)):
                word = Q.popleft()
                for i in range(len(word)):
                    for next_word in word_dict[word[:i]+"*"+word[i+1:]]:
                        #is reached
                        if next_word in visited2:
                            pathes1 = []
                            pathes2 = []
                            Path_generator(word, visited1, is_forward, pathes1)
                            Path_generator(next_word, visited2, not is_forward, pathes2)
                            if not is_forward:
                                pathes1, pathes2 = pathes2, pathes1
                            for path_forward in pathes1:
                                for path_backward in pathes2:
                                    result.append(path_forward+path_backward)
                            continue
                        #else
                        if next_word not in visited1:
                            Q.append(next_word)
                            level_dict[next_word].append(word)
            visited1.update(level_dict)
                        

        def Path_generator(node, visited, is_forward, pathes, path=[]):
            path.append(node)
            #End condition
            if not visited[node]:
                if is_forward:
                    pathes.append(path[::-1])
                else:
                    #needed to append COPY of path
                    pathes.append(path[:])

            for parent_node in visited[node]:
                Path_generator(parent_node, visited, is_forward, pathes)
            #"We must be able to undo each action when we backtrack" by Prof.Yook
            path.pop()

        #Path Generator

        #Conduct bidrictional search
        while Q_forward and Q_backword and not result:
            if len(Q_forward) <= len(Q_backword):
                Proceed(Q_forward, visited_forward, visited_backward, True)
            else:
                Proceed(Q_backword, visited_backward, visited_forward, False)
        
        return result

    
        

print(Solution().findLadders("hit", "cog", ["hot","dot","dog","lot","log","cog"]))