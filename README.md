# Paibi (排比) Student Essay Dataset

**Authors and Contributors**: 
* Stephen Bothwell, David Chiang (University of Notre Dame)
* Wei Song, Tong Liu, Lizhen Liu, Hanshi Wang (Capital Normal University)
* Ruiji Fu (Iflytek Research Beijing)
* Ting Liu (Harbin Institute of Technology)

**Maintainer**: Stephen Bothwell

## Summary

The Paibi Student Essay (henceforth abbreviated PSE) dataset originates from Song *et al.*'s work, ["Learning to Identify Sentence Parallelism in Student Essays"](https://aclanthology.org/C16-1076/).
At the current time, this dataset consists of 409 essays annotated toward the study rhetorical parallelism, 
especially in the context of automated essay evaluation. Work on this dataset was later integrated into the iFlyEA software
as described in the paper ["IFlyEA: A Chinese Essay with Automated Rating, Review Generation, and Recommendation"](https://aclanthology.org/2021.acl-demo.29/) (Gong *et al.* 2021).

A revised subset of it, known as the PSE-I (or "inside") subset, also features in the work "Introducing Rhetorical Parallelism Detection: A New Task with Datasets, Metrics, and Baselines" (Bothwell *et al.* 2023). 
It incorporates all 409 essays, both removing and adding some annotations to suit the task definition at hand.

Both the original PSE dataset and the augmented PSE-I subset are available in this repository and are described in more detail below.

### Use

This section is a work in progress.

**TODO**: add appropriate licensing.

## Contents

In this section, we describe the many versions of our data that we make available here.
We partition this discussion into two sections, detailing both the original version of the PSE dataset 
and its augmented subset, PSE-I, in turn.

### Original Version

Each of the original 544 essays were collected from various senior high school students in China who took a mock exam. 
These students wrote either narrative or argumentative essays.
Upon receiving these essays, two labelers annotated rhetorical parallelism between sentences.
They were equipped with a concise definition of parallelism: "two or more coherent text spans (phrases or
sentences), which have similar syntactic structures and related semantics, and express relevant content or emotion
together" (Song *et al.* 2016).
Thirty of the essays were marked up by both annotators; these annotators achieved an inter-annotator agreement of .71 (via Cohen's κ).

#### XML Structure

The original dataset contains a variety of organizational and linguistic data alongside its parallelism annotations.
It has a total of six XML tag types, and we cover each of them below:
* `<xml4nlp>`: Each document is grouped inside this tag; it has no adjoining metadata. 
* `<doc>`: The organization of the text is contained within this tag. Its attributes may possess some high-level information about the essay. 
For instance, it may list the numerical score(s) that the essay received. 
Each essay could have one overall score (`score`); it could also have multiple scores awarded by up to three different scorers (noted via the values `score1`, `score2`, and `score3`) and an aggregation of those scores. 
* `<para>`: These tags designate paragraphs in a document. 
They have `id` values which enumerate them; such values increment sequentially and start from 0. 
* `<scrawl>`: These tags are self-contained and indicate edits to the essays. **[[TODO: Clarification?]]**
* `<sent>`: These tags indicate sentences in a paragraph.
They have an `id` attribute; it functions as the `<para>` tag's does. 
They also have a `cont` attribute which provides the contents of a given indicated sentence.
Finally, they maintain a `type` tag whose contents will be described in more detail below.
The Language Technology Interface (Che *et al.* 2010) was employed to segment sentences (as well as to tokenize the text and to provide linguistic data for this dataset; we elaborate on such matters below).
* `<word>`: Each `<sent>` contains words which indicate the actual tokens of the sentence. 
Each `<word>` has a `cont` field with its corresponding token. It also possesses an `id` attribute which proceeds as `<para>`'s and `<sent>`'s do.
Finally, it contains a variety of other linguistic metadata to be discussed below.

#### Parallelism Annotation Scheme

Sentences in this dataset have a small set of tags they use to indicate parallel structure. 
These tags appear in the `type` field of `<sent>` tags, as annotations were done on the sentence level.

Possible tags are sevenfold (not including blank and nonexistent annotations):
- `inParaPaibiB`: the sentence begins a parallelism which exists completely in the given paragraph.
- `inParaPaibiI`: the sentence is within a parallelism which exists completely in the given paragraph.
- `inParaPaibiE`: the sentence is the last in a parallelism which exists completely in the given paragraph.
- `outParaPaibiB`: the sentence begins a parallelism which proceeds outside the given paragraph.
- `outParaPaibiI`: the sentence is within a parallelism which proceeds outside the initial paragraph.
- `outParaPaibiE`: the sentence is the last in a parallelism which proceeds outside the initial paragraph.
- `inSentenceBIE`: the sentence holds a complete parallelism within it.

These annotations link together sequentially either in a chain of `in`-based or `out`-based tags, proceeding from `B` to (potentially) `I` to `E`.  However, there are exceptions to this rule.
For example, an `inSentenceBIE` tag may link with another parallelism that has thus far contained individual sentences. 
Tags may have nonlinear relationships (*e.g.*, essay `010110237.xml`), causing connections to become less clear without manual review.

#### Other Metadata

Each `<word>` tag in this format has a variety of linguistic data attached to it sourced from the Language Technology Platform (Che _et al._ 2010). 
Such tags include:
* `pos`: the part-of-speech tag for the given token.
* `ne`: the named entity tag (in BIOES format) for a given token.
* `parent`: the `id` of the current word's parent word in the sentence's dependency tree. It is -1 if no parent exists.
* `relate`: the tag for the syntactic relationship represented in the dependency tree for the given token.

#### Provided Files

In this repository, we provide four variations on the original PSE dataset. 
All variations are contained in the `data/original` directory. 

In the `preserved` subdirectory, we provide the original data.
Meanwhile, in the `corrected` subdirectory, we manually reviewed and altered some tags (when possible) that seemed not to be as intended, as they broke apparent linear connections between tagged sentences. 
We also noted other files which maintained such nonlinearity issues or are otherwise dubious. 
These include `12.xml` and `367.xml`.

Each of these subdirectories contain two further subdirectories. 
On the one hand, the `full` subdirectory in each contains all the tags and metadata described above. 
On the other hand, the `abbreviated` subdirectory only contains sentence-level data. 
The text in `cont` is moved inside each `<sent>` element, and only parallelism tags are retained. 
While the former representation gives a fuller view of the data, the latter may supply an easier format for reviewing the data strictly relevant for parallelism detection.

### Augmented Subset (PSE-I)

#### XML Structure

The augmented subset of the data retains the same XML tags as the original version.
The major differences between the original dataset and this subset lie in the way in which the parallel structure is represented.

#### Parallelism Annotation Scheme

In the PSE-I subset's data, each `<word>` that is part of a parallelism has a `parallelism_id` and `branch_id`.
Both are numbered with their corresponding stratum (or level of nesting): 1.
Because the PSE-I dataset is flat--that is, no nested parallelisms exist--such numeration is not strictly necessary. 
We retained it to match the [ASP dataset](https://github.com/Mythologos/Augustinian-Sermon-Parallelisms)'s style of tokenized presentation and to preemptively cover potential expansions to the dataset.

Both `parallelism_id_1` and `branch_id_1` increment sequentially in document order. 
Following the original PSE dataset, `parallelism_id_1` starts at 0; however, following the ASP dataset, `branch_id_1` starts at 1.

In order to keep parallelisms local within the data, the parallelisms retained in this subset only consist of those with `in` tags in the original data. 
In other words, all `out` parallelisms (roughly 250 of them) are excluded. 
Simultaneously, to achieve higher granularity with regard to parallelisms in the data, we took two steps.
1. First, we annotated all `inSentenceBIE` tags to label the locations of internal branches.
Five annotators collectively performed this process on approximately 250 sentences, 
and their instructions for doing so via the `brat` annotation tool (Stenetorp *et al.* 2012) are given in the PDF located in the `data/augmented/procedure` subdirectory.
2. Second, we excluded all punctuation from the ends of parallelisms, as these are not critical to parallel structure: we argue that they only serve the role of delimiting sentences from one another.

#### Other Metadata

This version of the dataset retains all the metadata contained in the original version.
All the same nomenclature is used across both versions.

#### Provided Files

Our repository provides the data described here in the `full` subdirectory under `data/augmented`.

#### Statistics

The table below summarizes its base statistics. For exact definitions of *parallelism* and *branch* with regard to this version of the data, please see the paper by Bothwell *et al.* 2023.
Toward a basic understanding, consider a *branch* to be a continuous span of annotated text; 
then, consider a *parallelism* to be a group of said spans.

| Quantity       | Total   |
|----------------|---------|
| Documents      | 409     |
| Paragraphs     | 3,855   |
| Parallelisms   | 786     |
| Branches       | 2,153   |
| Branched Words | 25,529  |
| Words          | 241,203 |

Note that the word-based quantities are applied post-tokenization.

## Contributing

This repository is intended to provide a single, definitive version of this dataset for future work and research. 
However, if there are issues or mistakes with the data, we would be glad to investigate them. 
Please open an issue to start a conversation on the subject. 

Any future updates of the dataset will be tagged with a version number so as to make it easy to designate and compare results. 
The current version is `v1.0`.

## Citations

### Our Work

To cite this dataset, please refer to the following paper for the original data:

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

... and to the following paper for the augmented data (alongside the prior citation):
```
...
```


### Others' Work

We also provide citations of relevant scholarly works mentioned above. These are as follows:

```
@inproceedings{gongIFlyEAChineseEssay2021,
  title = {{{IFlyEA}}: {{A Chinese}} Essay Assessment System with Automated Rating, Review Generation, and Recommendation},
  booktitle = {Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: {{System}} Demonstrations},
  author = {Gong, Jiefu and Hu, Xiao and Song, Wei and Fu, Ruiji and Sheng, Zhichao and Zhu, Bo and Wang, Shijin and Liu, Ting},
  year = {2021},
  month = aug,
  pages = {240--248},
  publisher = {{Association for Computational Linguistics}},
  address = {{Online}},
  doi = {10.18653/v1/2021.acl-demo.29},
  abstract = {Automated Essay Assessment (AEA) aims to judge students' writing proficiency in an automatic way. This paper presents a Chinese AEA system IFlyEssayAssess (IFlyEA), targeting on evaluating essays written by native Chinese students from primary and junior schools. IFlyEA provides multi-level and multi-dimension analytical modules for essay assessment. It has state-of-the-art grammar level analysis techniques, and also integrates components for rhetoric and discourse level analysis, which are important for evaluating native speakers' writing ability, but still challenging and less studied in previous work. Based on the comprehensive analysis, IFlyEA provides application services for essay scoring, review generation, recommendation, and explainable analytical visualization. These services can benefit both teachers and students during the process of writing teaching and learning.}
}

@inproceedings{cheLTPChineseLanguage2010,
  title = {{{LTP}}: {{A Chinese}} Language Technology Platform},
  booktitle = {Coling 2010: {{Demonstrations}}},
  author = {Che, Wanxiang and Li, Zhenghua and Liu, Ting},
  year = {2010},
  month = aug,
  pages = {13--16},
  publisher = {{Coling 2010 Organizing Committee}},
  address = {{Beijing, China}}
}

@inproceedings{stenetorpBratWebbasedTool2012,
  title = {{{brat}}: A Web-Based Tool for {{NLP-assisted}} Text Annotation},
  booktitle = {Proceedings of the Demonstrations Session at {{EACL}} 2012},
  author = {Stenetorp, Pontus and Pyysalo, Sampo and Topi{\'c}, Goran and Ohta, Tomoko and Ananiadou, Sophia and Tsujii, Jun'ichi},
  year = {2012},
  month = apr,
  publisher = {{Association for Computational Linguistics}},
  address = {{Avignon, France}}
}
```