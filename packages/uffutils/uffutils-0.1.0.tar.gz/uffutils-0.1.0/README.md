# UFF Utils 

This library contains a set of pipeline tools for manipulating UFF files. It works a bit like this: 

```sh
uffutils modify my_original_file.uff my_subset_file.uff --node-step 100 --node-count 1000
$nodes = $(uffutils describe my_subset_file.uff --nodes-only)
uffutils modify my_file.uff my_output.uff `
    --node-selection $nodes `
    --scale-length 1000 `
    --to-global-frame `
    --rotate 90,90,90 `
    --translate 100,100,100
```

# The `inspect` command 

```sh 
uffutils inspect my_file.uff  # Nice overview 
uffutils inspect my_file.uff --property nodes --full # Full list of nodes
uffutils inspect my_file.uff --sets 0 # Description of dataset 0, including available properties
uffutils inspect my_file.uff --sets 1 --property r1,r2,r3 --mean
```

Basically, we have several options: 

```sh 
--full/--mean/--max/--summary  # Tells what to do with a range of numbers (default is summary)
--properties [string]  # What properties to focus on; if just one property is selected, no labelling is applied (default is all)
--sets [int] # What sets to focus on (default is None)
```

# Alternative implementation

I considered doing something with piping, but got stuck in the fact the the PyUFF library I'm using can't handle streams. It would've looking something like this: 

```sh
uffutils subset my_original_file.uff my_subset_file.uff --step 100 
uffutils subset my_file.uff - --nodes $(uffutils describe my_subset_file.uff --nodes) | 
uffutils scale - my_output.uff --length 1000 
```
