# Paibi Student Essay Dataset

The Paibi Student Essay (henceforth abbreviated PSE) derives from the work of Song *et al.* in their paper, "Learning to Identify Sentence Parallelism in Student Essays."
According to the original paper, this dataset contained 544 essays taken from mock exams of senior high school students. 
The PSE dataset currently consists of 403 of these essays.
Each essay is annotated for rhetorical parallelism between sentences. 
Of the original 544 essays, 30 were annotated by the two annotators, and a Cohen's kappa of .71 was attained for inter-annotator agreement.

Below, we describe the annotation scheme in this data.

## Annotation Scheme

Sentences in this dataset have a few possible tags to use to indicate parallel structure. 
This annotation falls under the `type` field inside the data's XML tag, and it labels the text in the `cont` (or contents) field.

Possible annotations are ninefold:
- inParaPaibiB: the sentence begins a parallelism which exists completely in the given paragraph.
- inParaPaibiI: the sentence is within a parallelism which exists completely in the given paragraph.
- inParaPaibiE: the sentence is the last in a parallelism which exists completely in the given paragraph.
- outParaPaibiB: the sentence begins a parallelism which proceeds outside of the given paragraph.
- outParaPaibiI: the sentence is within a parallelism which proceeds outside of the initial paragraph.
- outParaPaibiE: the sentence is the last in a parallelism which proceeds outside of the initial paragraph.
- inSentenceBIE: the sentence holds a complete parallelism within it.
- Blank: the sentence does not contain a parallelism.
- None: the sentence does not contain a parallelism, and it was not labeled with a `type` field. 

TODO: what else is worth adding?

# Citations

To cite this dataset, please refer to the following paper:

```
@inproceedings{songLearningIdentifySentence2016,
  title = {Learning to {{Identify Sentence Parallelism}} in {{Student Essays}}},
  booktitle = {Proceedings of {{COLING}} 2016, the 26th International Conference on Computational Linguistics: {{Technical}} Papers},
  author = {Song, Wei and Liu, Tong and Fu, Ruiji and Liu, Lizhen and Wang, Hanshi and Liu, Ting},
  year = {2016},
  month = dec,
  pages = {794--803},
  publisher = {{The COLING 2016 Organizing Committee}},
  address = {{Osaka, Japan}},
  abstract = {Parallelism is an important rhetorical device. We propose a machine learning approach for automated sentence parallelism identification in student essays. We build an essay dataset with sentence level parallelism annotated. We derive features by combining generalized word alignment strategies and the alignment measures between word sequences. The experimental results show that sentence parallelism can be effectively identified with a F1 score of 82\% at pair-wise level and 72\% at parallelism chunk level.Based on this approach, we automatically identify sentence parallelism in more than 2000 student essays and study the correlation between the use of sentence parallelism and the types and quality of essays.}
}
```
