major_scale_intervals = [2, 2, 1, 2, 2, 2, 1]
minor_scale_intervals = [2, 1, 2, 2, 1, 2, 2]

#Example: The root note or the 1 of the chord has a ranking of two
note_rankings = [2,1,3,2,3,1,2]
def get_degree(root,note,type = "major"):
    #set scale type
    if type == "major":
        scale = major_scale_intervals
    track = 0

    #check if note is root
    if root == note:
        return track
    
    #search to find wich scale dergree note is
    for i in scale:
        root+= i
        if root == note:
            return track
        
    #if note not in scale return -1
    return -1

def get_huristics_for_note(root,note,type,prev_note):
    #get position of note in scale
    scale_degree = get_degree(root,note,type)

    prev_scale_degree = get_degree(root,prev_note,type)
    
    if scale_degree == -1:
        return 0
    
    
    return note_rankings[scale_degree]