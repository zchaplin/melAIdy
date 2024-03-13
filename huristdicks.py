
scale_intervals = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2]
}
#Example: The root note or the 1 of the chord has a ranking of two
note_rankings = [1,2,0,1,0,2,1]


def get_degree(root,note,type = "major"):
    #set scale type
    
    scale = scale_intervals[type]
    track = 0
    root = root%12
    note = note%12
    if note < root:
        note +=12
    #check if note is root
    if root == note:
        return track
    #search to find wich scale dergree note is
    for i in scale:
        track += 1
        root += i
        if root == note:
            return track
        
    #if note not in scale return -1
    return 100

def get_huristics_for_note(root,note,type,prev_note):
    #get position of note in scale
    scale_degree = get_degree(root,note,type)

    prev_scale_degree = get_degree(root,prev_note,type)
    
    if scale_degree == 100:
        return 100
    
    return note_rankings[scale_degree-1] + int(abs((scale_degree - prev_scale_degree)))

def get_huristics_for_scale(root,type,prev_note):
    output = {}
    for i in scale_intervals[type]:
        output[root+i] = get_huristics_for_note(root,root+i,type,prev_note)
    return output
        
