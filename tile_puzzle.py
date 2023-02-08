import numpy as np
from queue import Queue, deque
import time


'''
    ## This solution has flattened the 2-D matrix of the puzzle into a 1-D row-wise vector:
    # So if any of the states is:
    # 1 3 5
    # 2 4 0
    # 7 8 6
    # then the solution will treat it as (1,3,5,2,4,0,7,8,6)

    ## The datastructure to represent the each node (intermediate state) of the search-tree is so
    # chosen that it contains a map/dictionary so as to accomodate the state_pattern, string of actions from the init_state that has led to that state, and its index.
    # example: Node = {'pattern': (1,6,5,4,2,0,7,3,8), 'path': 'LDRULDR', 'index': 30} , where L,R,U,D are left, right, up and down actions respectively.
'''

class TilePuzzle:

    def __init__(self, init_state):
        self.init_state = init_state
        self.total_numbers = len(init_state)
        self.target_state = self.get_target_state()
        self.matrix_dim = int(np.sqrt(self.total_numbers))
    
    #########################################################################
    
    def solve(self):
        if self.target_state == self.init_state:
            print('The tiles are already arranged.')
            return

        ## Check for solvability of the state first
        if not self.is_state_solvable(self.init_state):
            print('Given state is not solvable!')
            return

        init_state_node = {'pattern': self.init_state, 'path': '', 'index': 1}
        solution_state = {}

        state_queue = Queue()
        visited_states_set = set()

        visited_states_set.add(init_state_node['pattern'])
        state_queue.put(init_state_node)
        
        count = 0
        total_nodes_generated = 1

        is_target_state_found = False
        adj_map = {}
        child_parent_map  = {1: 0}

        msg_queue = Queue()
        self.init_msg_queue(msg_queue)

        print("\nPlease wait while the solver finds a solution for you...\n")
        start = time.clock()
        while not (state_queue.empty() or is_target_state_found):
            count +=  1
            if (not msg_queue.empty()) and (count % 150000 == 0):
                print(msg_queue.get())
            
            current_state = state_queue.get()
            visited_states_set.add(current_state['pattern'])
            
            next_states = self.get_next_states(current_state, adj_map, total_nodes_generated)
            total_nodes_generated = total_nodes_generated + len(next_states)

            adj_map[current_state['pattern']] = next_states
            
            for state in next_states:
                if self.target_state == state['pattern']:
                    print('Found!', 'Actions to be taken: ', state['path'])
                    solution_state = state
                    is_target_state_found = True
                elif state['pattern'] not in visited_states_set:
                    state_queue.put(state)
                
                # To map the parent node for a particular child node
                child_parent_map[state['index']] = current_state['index']
              
        end = time.clock()
        if not is_target_state_found:
            print("Target state not found")
        else:
            print(count, '=> Time taken:', end-start, 'seconds')
            self.write_to_Nodestxt_file(visited_states_set)
            self.write_to_NodesInfotxt_file(child_parent_map, solution_state['index'])
            self.write_to_nodePathtxt_file(solution_state)

    #########################################################################

    def get_next_states(self, state, adj_map, total_nodes_generated):
        if state['pattern'] in adj_map:
            next_states = adj_map[state['pattern']]
        else:
            # [R L D U] with (0,0) at top left corner
            actions = {'R': [0, 1], 'L': [0, -1], 'D': [1, 0], 'U': [-1, 0]}
            
            next_states = []
            
            index_of_zero = state['pattern'].index(0)
            
            pos_zero = [int(index_of_zero/self.matrix_dim), int(index_of_zero % self.matrix_dim)]
            
            for ind, action in enumerate(actions):
                new_pos_zero = np.add(pos_zero, actions[action])
                if (self.is_position_valid(new_pos_zero)):
                    next_states.append(
                        {
                        'pattern': self.move_zero_and_get_new_state(state['pattern'], index_of_zero, new_pos_zero), 
                        'path': state['path'] + action
                        })

        for ind, state in enumerate(next_states):
                state['index'] = total_nodes_generated + (ind + 1)
        return next_states

    #########################################################################
    
    def is_position_valid(self, position):
        return (position[0] in range(0,self.matrix_dim) and position[1] in range(0,self.matrix_dim))
    
    
    def move_zero_and_get_new_state(self, state, old_index_zero, new_pos_zero):
        new_index_zero = (self.matrix_dim*new_pos_zero[0]) + new_pos_zero[1]
        
        num_list = list(state)
        temp = num_list[new_index_zero]
        num_list[new_index_zero] = 0
        num_list[old_index_zero] = temp
        
        result_state = tuple(num_list)
        return result_state

    #########################################################################

    '''
        ## Given state is solvable if:
            N is even
                and, zero is in even row position from bottom
                    and, number of inversions are odd
                or, zero is in odd row position from bottom
                    and, number of inversions are even
            or, N is odd
                and, number of inversions are even
    '''
    def is_state_solvable(self, state):
        is_total_numbers_even = (self.total_numbers % 2 == 0)
        row_position_zero = (state.index(0))/self.matrix_dim
        inv_count = 0
        for i in range(0, self.total_numbers):
            for j in range(i+1, self.total_numbers):
                if (state[i] != 0 and state[j] != 0 and (state[i] > state[j])):
                    inv_count = inv_count + 1
        
        is_num_inv_even = (inv_count % 2 == 0)
        
        if is_total_numbers_even:
            if (row_position_zero % 2 == 0):
                return not is_num_inv_even
            else:
                return is_num_inv_even
        else:
            return is_num_inv_even
    
    #########################################################################

    def write_to_Nodestxt_file(self, visited_states_set):
        with open('Nodes.txt', 'w+') as nodes_file:
            for state in visited_states_set:
                nodes_file.write(self.get_state_string(state))
    
    def write_to_NodesInfotxt_file(self, child_parent_map, soln_ind):
        node_info_list = []
        child_ind = soln_ind
        parent_ind = child_parent_map[soln_ind]
        while parent_ind:
            node_info_list.append((child_ind, parent_ind))
            child_ind = parent_ind
            parent_ind = child_parent_map[child_ind]

        node_info_list.append((1,0))
        node_info_list.reverse()

        with open('NodesInfo.txt', 'w+') as nodes_info_file:
            for node in node_info_list:
                node_str = str(node[0]) + " " + str(node[1]) + '\n'
                nodes_info_file.write(node_str)
        
    def write_to_nodePathtxt_file(self, solution_state):
        actions = {'R': [0, 1], 'L': [0, -1], 'D': [1, 0], 'U': [-1, 0]}
        soln_path = solution_state['path']
        state_pattern = self.init_state
        with open('nodePath.txt', 'w+') as nodePath_file:
            nodePath_file.write(self.get_state_string(state_pattern)) 
            for action in soln_path:
                index_of_zero = state_pattern.index(0)
                pos_zero = [int(index_of_zero / self.matrix_dim), int(index_of_zero % self.matrix_dim)]
                new_pos_zero = np.add(pos_zero, actions[action])
                state_pattern = self.move_zero_and_get_new_state(state_pattern, index_of_zero, new_pos_zero)
                nodePath_file.write(self.get_state_string(state_pattern))

    #########################################################################
           
    def get_state_string(self, state):
        state_str = ''
        for i in range(0, self.matrix_dim):
            for j in range(0, self.matrix_dim):
                state_str += " " + str(state[i + j*self.matrix_dim]) 
        return state_str + '\n'

    def get_target_state(self):
        target_numbers_list = [num for num in range(1, self.total_numbers)]
        target_numbers_list.append(0)
        return tuple(target_numbers_list)

    
    def init_msg_queue(self, msg_queue):
        with open('msgs.txt', 'r') as msg_file:
            msg_queue.queue = deque(msg_file.readlines())