## Approach

Replace links and images with a special marker in the markdown that the llm sees and replace them later.


## Files
`split_md.py`: all the code

`allen-jan-part-1.md`: a halfway split of the full allen paper because the full one would get 1 error in the middle and break the ordering of the images

`allen-jan-2024.md`: the full allen paper used

`aakash.md`: the aakash paper used

`aakash_image_extracted.json`: aakash paper -> json with extracted images

`allen_image_extracted.json`: allen part 1 paper -> json with extracted images

`all_question.md`: the inital step done on the allen paper where image tags are replaced with a placeholder

`tagged_questions.json`: old allen -> json without extracted images

`test_questions.json`: file to test any small results
