class HashTableEntry:
    """
    Linked List hash table key/value pair
    Node class to store key value pair of the link list
    each node has string as key value pair and pointer 
    to the the next node in case there is collision
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity=8):
        # Your code here
        self.capacity = capacity
        #assiging list for the hash table
        self.list_hashtable= [None for i in range(self.capacity)]
        self.count =0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
       
        return  self.capacity #len(self.list_hashtable)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        #load factor = (No. of item in the hash table)/total no of slots
        # items=0
        # for i in range(self.capacity):
        #     existing_node = self.list_hashtable[i]
        #     if existing_node:
        #         while existing_node:
        #               items +=1
        #               existing_node=existing_node.next


        load_factor = self.count/self.capacity 
        return load_factor


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        It uses bit manipulation and prime numbers 
        to create a hash index from a string
        """
        hash = 5381
        byte_array = key.encode('utf-8')
        for byte in byte_array:
            # the modulus keeps it 32-bit, python ints don't overflow
             hash = ((hash * 33) ^ byte) % 0x100000000
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        #calculate index to store  string(key)in the list
        list_index = self.hash_index(key)
        #create a link list at that index to store bucket of key value pair
        #create a node with given key value pair
        new_node = HashTableEntry(key, value)
        # check if there is a node at that index of the list
        existing_node = self.list_hashtable[list_index]
        if existing_node:
            while existing_node:
                #compare key and value at that index with the new_node 
                if existing_node.key == new_node.key:
                    #replace the value if it is already exist
                    existing_node.value = value
                    return
                last_node = existing_node
                existing_node = existing_node.next
            #if we didn't find the value in the bucket
            #put the value at the end of bucket
            last_node.next = new_node
            self.count +=1
        else:
            #store new_node at  that index of the list
            self.list_hashtable[list_index] = new_node
            self.count +=1
        load_factor = self.get_load_factor()
        if load_factor >0.7:
            self.resize(int(self.capacity *2))




    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        #calculate index to find  string(key)in the list
        list_index = self.hash_index(key)
        # check if there is a node at that index of the list
        existing_node = self.list_hashtable[list_index]
        if existing_node:
            #keep looking for the key in the bucket till the end
            prev_node = None
            while existing_node:
              
                if existing_node.key == key:
                    if prev_node:
                        prev_node.next = existing_node.next
                    else:
                        self.list_hashtable[list_index] = existing_node.next 
                prev_node = existing_node
                existing_node=existing_node.next
        else:
            print(f'waring: {key} not found')
        


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """  
        #calculate index to find string(key)in the list
        list_index = self.hash_index(key)
        # check if there is a node at that index of the list
        existing_node = self.list_hashtable[list_index]
        if existing_node:
            while existing_node:
                #compare key and value at that index with the new_node 
                if existing_node.key == key:
                    return existing_node.value
                existing_node = existing_node.next
        else:
            return None



    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """   
        new_list = [None for i in range(new_capacity)]
        old_capacity = self.capacity
        self.capacity = new_capacity
        old_list = self.list_hashtable
        self.list_hashtable = new_list
        for node in old_list:
            if node:
                self.put(node.key, node.value)

               


            



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    load_factor = ht.get_load_factor() 
    print(load_factor)
    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()
     
    load_factor = ht.get_load_factor() 
    print(f"\nResized from {old_capacity} to {new_capacity}.\n")
    print(load_factor)
    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
