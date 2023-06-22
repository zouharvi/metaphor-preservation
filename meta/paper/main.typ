#import "template.typ": *
#import "tablex.typ": tablex, hlinex, vlinex, colspanx, rowspanx

#let TODO(body) = {text(fill: red)[TODO: #body] }
#let CODO(body) = {text(fill: red)[CITE TODO: #body] }

#show: project.with(
  title: [Metaphor Preservation in Machine Translation and Paraphrasing],
  authors: (
    (
      name: "Vilém Zouhar",
      organization: "ETH Zürich",
      email: "vzouhar@ethz.ch",
      misc1: "Report",
      misc2: "June 2023 (v1)",
    ),
  ),
  bibliography-file: "bibliography.bib",
  abstract: [
    Metaphors play a crucial role in human communication.
    Improving the handling of metaphors in NLP will enhance the quality and accuracy of cross-lingual communication, benefiting various applications such as multilingual chatbots, localization, and cross-cultural understanding.
    This paper reports an evaluation that focuses on the analysis of metaphor presence and preservation in machine-translated and paraphrased texts.
    The results suggest that textual language models do not have access to the metaphorical meaning and do not fully understand this literal device.
    They are not sensitive to the subtle differences between various paraphrases but can be used for the rudimentary analysis of machine translation output, which varies greatly with respect to metaphor preservation.
    //To this end, I propose a novel scoring mechanism, Metaphor Preservation Index (MPI), which quantifies the extent to which metaphors are preserved.
    //The results confirm that higher-quality MT systems struggle less with metaphor preservation and that paraphrases are able to deal with metaphors easily.
  ]
)
//department: [Department of Mathematics],
//location: [Columbia, SC 29208],
//url: "www.math.sc.edu/~howard"
//date: [June, 2023],

/*
#box(fill: rgb("#dddd"), inset: 10pt, radius: 10pt)[
  *Original assignment* #linebreak()
  #set text(size: 10pt, top-edge: "x-height")
  #TODO
]
*/

#align(right)[
// force to be inline
#box(width: 5mm, image("img/github-mark.svg"), baseline: 1.4mm) #h(1mm)
#link("https://github.com/zouharvi/metaphor-preservation")[github.com/zouharvi/metaphor-preservation]
]

#v(-2mm)
= Introduction

Metaphors allow for the conveyance of complex ideas and abstract concepts, and appear in most natural languages #cite("lakoff1980metaphors", "van1981limits").
However, when it comes to translation and paraphrasing tasks, the preservation of metaphors poses a challenge.
This paper investigates the extent to which machine translation (MT) and paraphrasing models can maintain the pragmatics and nuanced meaning carried by metaphors.
Specifically, I lay out two evaluation dimensions: if the overall meaning and sentiment are preserved and if the output also contains the metaphor.
/*
This paper is structured as follows:
- *@subsec:metaphor_def*: Definition of metaphors in the context of NLP
- *@subsec:philosophical_setting*: Connection to the philosophy of language processing
- *Sections: @sec:related[], @sec:data[], and @sec:model[]*: Related works, data and model descriptions
- *@sec:experiment*: Experiment setup and evaluation
- *@sec:end*: Discussion and conclusion
*/
Modern NLP perform very well both in style and meaning preservation.
Nevertheless, by examing the two dimensions individually, we gain insight into the various failure modes and where modern evaluation metrics fall short.
An advantage of this approach is that it does not require reference translations or paraphrases of the metaphors, which is a very sparse resource.#footnote[To my knowledge, no parallel metaphor translation data are available.]

The task is of dual nature: evaluating the sensitivity of evaluation models and using them to evaluate paraphrasers and machine translation systems.
Negative results are thus difficult to attribute directly to one of those.
Nevertheless, through especially qualitative analysis, a specific large language (GPT-based) model used for evaluation seems to be inadequate for evaluating sentence paraphrases.
However, it is able to capture catastrophic mistranslations of metaphorical meaning, which warrants further investigation into its usage for the evaluation of NLP models.

#figure(
  image("img/car_transmission.svg", width: 100%),
  caption: [Transmitting meaning of a message while having to change the surface-level text form. The messenger is possibly an agent who may not understand language and have access to the metaphorical meaning. Two things need to be checked: (1) _Is the metaphor still there_ and (2) _is the meaning of the metaphor the same?_],
) <car_transmission>


#pagebreak()

== Metaphors and NLP Transmission
<subsec:metaphor_def>

There are many ways to formally define metaphors, for example using structuralist semantics #cite("greimas") or use-is-meaning theory #cite("shibles").
The particular formalism is not important in this case and instead, I provide a brief explication of what metaphors may be.
A metaphor is a figure of speech that involves the use of a word or phrase in a way that extends its literal meaning, by drawing a comparison between two unrelated concepts or objects #cite("kovecses2017levels").
Metaphors typically use a source domain (the concept or object being used metaphorically) and a target domain (the concept or object to which the source domain is being compared).
For example, in _time is money_, we use the attributes of _money_, which can be _valuable, spent_, or _saved_ and apply it to _time_, which can be _valuable, spent_, or _saved_ as well.
There are many reasons why metaphors are widely used in language:

#v(2mm)
- *Conceptualization*: Metaphors facilitate the understanding of abstract or complex concepts by mapping them onto more familiar or concrete domains. They allow listeners to make sense of unfamiliar ideas by drawing on their knowledge and experiences from the source domain. #cite("kovecses2017levels")
- *Communication*: They can also evoke vivid imagery and emotional responses, making language more engaging, memorable, and persuasive. They can also express otherwise a very nuanced extra-channel information, such as attitudes or beliefs. #cite("keysar1992metaphor", "taylor2018problem")
- *Aesthetic*: Metaphors are also fundamental to creative and poetic expression and allow for the exploration of unconventional associations, juxtaposing disparate domains and generating new insights or perspectives. They encourage creative thinking and contribute to the artistic and expressive dimensions of language. #cite("camp2007showing")

#h(1em)
This work, however, does not make use of any of these distinctions.
Instead, it conceptualizes text in communication as mostly a latent object where only the lexical layer can be observed.
The meaning (literal or metaphorical) is then layered on top.
NLP operations, whose goal is to transform the surface form, while preserving the meaning (e.g. paraphrasing or machine translation), can inadvertently change the deeper meaning (see @car_transmission for an illustration).
Note that metaphors are not the only linguistic device which deals with latent meaning, but are the easiest to deal with in the context of NLP experiments because of data availability.

In the example in @metaphor_example, we consider four _translation_ transformations.
They each differ in whether the result also contains a metaphor and whether the meaning is matching the source.
The meaning of the metaphor is that a roller coaster ride composes of ups and downs, which map to good and low moments in life.
While the first translation is very literal, it represents the source faithfully both in terms of the metaphor and the meaning.
The second translation does not contain the metaphor but rather writes out the meaning, which is still acceptable.
The third translation contains a metaphor which however alludes to a different aspect of life, such as its cyclicity.
Finally, the last translation does not contain a metaphor and also does not transfer the same meaning as the source.
From this, we can conclude that the matching meaning is the most important aspect (because trans. 2 > trans. 3), followed up with the metaphor presence (trans. 1 > trans. 2).
The admissibility of these translations also corresponds to the theory of metaphor translation by #cite("van1981limits").

#v(10mm)
#figure(
  tablex(
    columns: (auto, auto, auto, auto),
    align: center + horizon,
    auto-vlines: false,
    repeat-header: true,

    [*Source*], [*Translation*], [*Metaphor#linebreak() present*], [*Meaning#linebreak() matching*],

    rowspanx(4)[Das Leben ist wie eine Achterbahn],
    align(left)[Life is like a roller coaster.], [#sym.checkmark], [#sym.checkmark],
    align(left)[Life can feel better or worse at times.], [#sym.times], [#sym.checkmark],
    align(left)[Life is like a merry-go-round.], [#sym.checkmark], [#sym.times],
    align(left)[Life is full of surprises.], [#sym.times], [#sym.times],
  ),
  caption: [Example of correct and incorrect metaphor/non-literal meaning translation.],
) <metaphor_example>
#v(5mm)

#h(1em) Despite not following a specific formalism, I bring forward a distinction observed by #cite("van1981limits") about the deadness and productivity of a metaphor.
Some metaphors, such as _"everybody"_ or _"harbour evil thoughts"_, have become lexicalized phrases (or _"dead"_) and their interpretation does not rely on constructive understanding of similarities between concepts, even if that was their origin.
Now those phrases acquired a static and uninventive meaning on their own which can likely be observed and learned without having any knowledge of the external world.
This would make it permissible for level 2 agents #cite("bisk2020experience") to perform the required tasks.
However, other types of metaphors, which are more inventive and appear less frequently, still require some additional knowledge and further processing in order to be understood.
In poetry, these types of inventive metaphors are taken to their extremes.

It can happen that the true meaning of an utterance is indeed its lexical one and not a metaphorical one.
For example _"you are feeding a fed horse"_ may indeed refer to someone trying to feed a horse that is already full and not that someone is performing some action in vain.
This distinction may be easily disambiguated by the context but may still pose problems for some agents whose task is to find the meaning of the utterance.

== Philosophical setting
<subsec:philosophical_setting>

Consider the octopus test #cite("bender2020climbing") but with a more complex setup where two communicators, who do not speak the same language, are stranded on two separate islands and want to communicate.
To their luck, there is a bilingual fisherman who does not want to save them but agrees to transmit and translate messages between the two communicators.
Now assume that there are layers of meaning in an utterance, ranging from the surface to deeper level #cite("chomsky1971deep").
In order for the fisherman to succeed at the task they promised, they need to have some access to the deeper level.
In the spirit of #cite("bender2020climbing"), the fisherman must have a mapping from the surface to the deeper level in both the input and output spaces (e.g. source and target languages) and assure, that both forms map to the same meaning.
It may then happen, that the fisherman is actually not a human, but an octopus in disguise.

This role of a transmitter is often assumed by modern NLP tools, such as machine translation and paraphraser.
These tools, like the octopus in #cite("bender2020climbing"), likely do not know the full mapping function.
Nevertheless, they may still have observed the fisherman doing their job and therefore imitate some of their behaviour (e.g. learning to translate metaphors).
To what extent the octopi or the tools are able to achieve this task is the topic of this article.
The focus is on metaphors as a specific type of deeper-level meaning because they are problematic even for skilled workers, such as translators, and they exemplify the problem of accessing the true meaning of an utterance in practice #cite("van1981limits").

= Related work
<sec:related>

== Metaphor Translation & Paraphrasing

The preservation of additional, non-literal meaning in machine translation was explored for poeticness #cite("seljan2020human", "zouhar2022poetry"), ambiguity #cite("parida2019hindi", "stahlberg2022jam"), formality #cite("niu2017study", "viswanathan2020controlling"), emotion #cite("troiano2020lost", "kajava2020emotion"), creative shifts in literature translation #cite("toral2018level", "guerberof-arenas_impact_2020", "Humble_2019") and puns and other pragmatics #cite("farwell2006pragmatics", "carvalho2022memes").

There are some works that already deal with machine translation of metaphors #cite("alkhatib2018paraphrasing") and machine-translated translation #cite("schaffner2020translation", "vinall2021down", "massey2021re").
All the evaluations were either done by manual human inspection or using standard automated metrics, such as BLEU #cite("papineni2002bleu") or METEOR #cite("banerjee2005meteor"), which do not take meaning preservation specifically into account.
Nevertheless, this article deals with primarily the _evaluation_ of metaphor preservation.

The evaluation of metaphor paraphrases is problematic out of the lack of reference data #cite("mao2022metapro").
Still, paraphrasing metaphors into their literal meaning is often used for metaphor interpretation #cite("shutova2010automatic","bollegala2013metaphor").

== Metaphor Detection & Preservation Evaluation

The _landmark method_ #cite("kintsch2000metaphor") was already used in modern NLP to examine large language models #cite("pedinotti2021howling").
It is based on comparing the vector representation of predicates in the simile.#footnote[Similes are figures speech closely related to metaphors. They are usually in the form of _"X is like Y"_ where a non-literal meaning of _Y_ is meant.]
For example, consider: _"As #underline[straight] as an #underline[arrow]"_.
Then, words related to the literal meaning of the predicates are sampled, e.g. _direct_ and _archery_ and their vector representations are compared with the contextualized representations in the original utterance.
Despite the ingenuity of this and similar #cite("do2016token", "su2020deepmet") approaches, it provides an intrinsic evaluation perspective, while the goal of this article is to examine the models from an extrinsic perspective, such as using language models #cite("neidlein2020analysis", "aghazadeh2022metaphors").
Notable is the distinction between metaphor detection at _token-level_ and at _sentence-level_.
This work deals only with the latter.

= Data & Models
<sec:data>

For the experiments, I leverage two types of data, dubbed Trofi #cite("birke2006clustering", "birke2007active") and FMO #cite("zayed2020figure").
The latter contains a reference paraphrase of the metaphor so that the meaning is the same but a metaphor is not used (see @tab:data for an example).
Although the FMO dataset is more suitable because it contains corresponding pairs, it is more artificial than the Trofi dataset which is taken from authentic data.
For this reason, I include both in this investigation.
Note that due to costs the datasets are subsampled and all the data is in English.
For simplicity, sentences marked as containing metaphorical phrases are referred to as _metaphorical sentences_ and the rest as _literal sentences_.

#v(3mm)
#figure(
  tablex(
    columns: (auto, auto, 11.5cm),
    align: left + horizon,
    auto-vlines: false,
    repeat-header: true,

    [*Dataset*], [*Size*], [*Example*],
    [Trofi], [200 (met.) + #linebreak() 200 (lit.)], [
      *Literal*: _"The yellow beta carotene pigment absorbs blue not yellow laser light"_ #linebreak()
      *Metaphor*: _"But Korea s booming economy can absorb them, economists say"_
    ],
    [FMO], [200 (pairs)], [
      *Literal*: _"She wrote powerful and painful words"_ #linebreak()
      *Metaphor*: _"Her pen was a knife"_
    ],
  ),
  caption: [Summary of dataset sizes and examples. The _Trofi_ dataset contains individual literal or metaphorical sentences while _FMO_ contains pairs of metaphorical sentences and the corresponding literal paraphrasing.],
) 
<tab:data>
#v(5mm)

== Translation and Paraphrasing Models

To increase the relevancy of this study, I include a mixture of publicly available closed-source and open-source systems which are commonly used and are nearing state-of-the-art.#footnote[Google Translate and DeepL were accessed on June 20th 2023 via paid API.]
The target translation languages from English are German and Czech.
GPT-based model was intentionally not used for translation or paraphrasing to avoid the error of the same model evaluating itself, like in #cite("zhang2023exploring").

#v(2mm)

#box(width: 54%)[
*Translation:*
//- ChatGPT #link("https://chat.openai.com/", "[chat.openai.com]") #footnote[Zero-shot translation with the prompt _"Translate the following text #TODO[]"_.]
- Google Translate #link("https://translate.google.com/", "(translate.google.com)")
- DeepL #link("https://www.deepl.com/translator", "(deepl.com/translator)")
//- QuillBot #link("https://quillbot.com/", "[quillbot.com]")
- T5-large (#cite("2020t5", brackets: false), #link("https://huggingface.co/t5-large", "huggingface"))
- NLLB-200-1.3B (#cite("costa2022no", brackets: false), #link("https://huggingface.co/facebook/nllb-200-1.3B", "huggingface"))
]
#box(width: 50%)[
*Paraphrasing:*
//- QuillBot #link("https://quillbot.com/", "(quillbot.com)")
- Pegasus Paraphrase #link("https://huggingface.co/tuner007/pegasus_paraphrase", "(huggingface)")
//- ChatGPT #link("https://chat.openai.com/", "(chat.openai.com)") #footnote[Zero-shot paraphrasing with prompt _"Paraphrase the following text so that its meaning is identical and the style is preserved"_.]
- Bart (#cite("lewis2019bart", brackets: false), #link("https://huggingface.co/eugenesiow/bart-paraphrase", "huggingface"))
- Parrot on T5 #link("https://huggingface.co/prithivida/parrot_paraphraser_on_T5", "(huggingface)")
- Paws on T5 #link("https://huggingface.co/Vamsi/T5_Paraphrase_Paws", "(huggingface)")
]

#v(3mm)
== Metaphor Evaluation Models
<sec:evaluation_models>

For the evaluation of metaphor presence and meaning preservation in both translation and paraphrasing, `GPT3.5-turbo` is used with the following prompts.#footnote[The total price for the evaluation using this OpenAI model was 5\$.]
The result for each is a number between 1 and 5 (see usage details in code).
- _"You are a helpful and austere assistant for metaphor detection in text. Reply using only a single number 1 to 5 scale and nothing else."_
- _"You are a helpful and austere assistant for detecting how much is the true meaning preserved. Reply using only a single number 1 (not at all) to 5 (completely, including style) and nothing else.\\nSource: $#sym.circle$\\nParaphrase: $#sym.circle$_"

#h(1em)
Recall from the introduction, that there is no reference translation or paraphrase for which traditional reference-based metrics could be used.
In the case of translation, it can be viewed as quality estimation, which is known to be feasible with GPT4 #cite("kocmi2023large").
Nevertheless, for the second point, a state-of-the-art sentence similarity system #link("https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")[`MiniLM-L12-v2`] is used.#footnote[This is used also for the translation evaluation in lieu of standard quality estimation systems, such as COMET #cite("rei2020comet"), because the sentence similarity is more important than translation quality.]
Its working closely reflects the introduced formalism by first computing a vector representation of the meaning of both the source and the output and then comparing the closeness of these two vectors.

= Experiment
<sec:experiment>

== Setup

The original data (400+400 sentences) was paraphrased using 4 models and translated into Czech and German using 4 other models, overall yielding $800 #sym.times 12 = 9600$ sentences.
Each of them is then evaluated (see @sec:evaluation_models) on metaphor presence and meaning preservation with respect to the original sentence both on scale 1 to 5.
The meaning preservation is also evaluated using cosine distance (rescaled to 1 - 5) between vector representations of the original and new sentence.

== Original Data Metaphor Presence

The distributions of assigned scores are shown in @base_violin.
At first glance, the distribution for literal and metaphorical sentences is very similar.
The average scores for Trofi are indeed 2.36 and 2.42 and for FMO 2.43 and 2.95, respectively.
On the sentence-level for FMO, in 43% was the metaphorical sentence rated higher than the literal one and in another 43% was the rating identical.
These results point at either (1) the datasets, specifically Trofi, not having large enough distinctions between sentence types or (2) the evaluation model not being sensitive enough.
@sec:paraphrasing_evaluation shows that the latter is the case, which points to a limitation of using current state-of-the-art large language models for evaluation.
Nevertheless, the results for FMO partially justify using this evaluation method for evaluating other NLP models based on if the metaphor is present.
Lastly, in some cases, the classification of metaphoricity in the dataset is questionable, such as _"Now you can fade off to sleep."_ (metaphor) and _"Now you can go to sleep."_ (literal).
In this case, the language model assigned metaphor presence scores of 1 and 5, respectively, contrary to our intuition.
It is, however, possible to argue that they are both metaphors, though the latter is lexicalized (dead).

#v(4mm)
#figure(
  image("img/base_violin.svg", width: 50%),
  caption: [Distribution of scores assigned for metaphor presence to the original sentences from the dataset.],
) <base_violin>
#v(4mm)

#pagebreak()

== Paraphrasing Evaluation
<sec:paraphrasing_evaluation>

Further investigations will use solely the FMO dataset, where the difference between sentence types is greater.
The models are evaluated on whether a metaphor is present, if the meaning is preserved and what the sentence similarity is to the original.
As an anchor for sentence similarity (1 to 5), consider the value 4.8, which is the average similarity between literal and metaphorical sentences in FMO.
The evaluation is performed on literal and metaphorical sentences separately.
The results are visualized in @fig:radar_paraphrasing with examples in @tab:examples_paraphrasing.

#figure(
  [
    #v(3mm)
    
    #box[#image("img/radar/paraphrase_bart.svg", width: 24.5%)]
    #box[#image("img/radar/paraphrase_parrot.svg", width: 24.5%)]
    #box[#image("img/radar/paraphrase_paws.svg", width: 24.5%)]
    #box[#image("img/radar/paraphrase_pegasus.svg", width: 24.5%)]
  ],
  caption: [
    Evaluation of paraphrasing models on 
    #box(fill: rgb("#9791c6"), inset: 1mm, baseline: 1mm)[literal] (left) and
    #box(fill: rgb("#ccabce"), inset: 1mm, baseline: 1mm)[metaphorical] (right)
    sentences. #v(3mm)
  ],
)
<fig:radar_paraphrasing>


#h(1em) Overall, the meaning of literal sentences seems to be preserved more than those of metaphorical sentences.
This is exemplified with the overall system quality.
For the better-performing one, BART, the averages are 4.7 and 4.6 and for Pegasus they are 4.5 and 4.1 for literal and metaphorical sentences, respectively.
Nevertheless, as Example 1 in @tab:examples_paraphrasing shows, it is unclear whether this is because of the language model bias or randomness.
There is otherwise very little variation in performance for paraphrasing models.
A natural question is whether the paraphrases are all equally good or whether the evaluation model is not sensitive enough.
In some cases, the differences are caused by the paraphraser outputting a near-identical sentence lexically, which naturally leads to perfect preservation (Example 2).
However, in some cases, such as Example 3, the sentence similarity uncovered a loss of meaning (feeling of being surrounded by an expanse of grass).

#figure(
  tablex(
    columns: (auto, 14cm),
    align: left + horizon,
    auto-vlines: false,
    repeat-header: true,

    [*Index*], [*Example*],
    align(center)[1], [
      *Source (literal)*: _"The boss will criticise me severely if the report arrives late."_ #linebreak()
      *Source (metaphor)*: _"The boss will eat me alive if the report arrives late."_ #linebreak()
      *Pegasus (literal)*: _"If the report arrives late, the boss will be critical of me."_ *(preservation 5)* #linebreak()
      *Pegasus (metaphor)*: _"If the report arrives late, the boss will eat me."_ *(preservation 2)* #linebreak()
    ],
    align(center)[2], [
      *Source (metaphor)*: _"The faculty meeting was a tragedy"_ #linebreak()
      *Pegasus*: _"The meeting was sad."_ *(preservation 1)* #linebreak()
      *BART*: _"The faculty meeting was a tragedy"_ *(preservation 5)* #linebreak()
    ],
    align(center)[3], [
      *Source (metaphor)*: _"we were sinking in an ocean of grass"_ #linebreak()
      *Pegasus*: _"we were in the grass"_ *(similarity 3)* #linebreak()
      *Parrot*: _"we were sinking in the grassy sea"_ *(preservation 5)* #linebreak()
    ],
  ),
  caption: [Examples of paraphrases of FMO sentences. #v(3mm)],
) 
<tab:examples_paraphrasing>

#v(8mm)

== Translation Evaluation
<sec:translation_evaluation>

In the case of machine translation, the differences between systems (in @fig:radar_translation) are, similarly, not blatant.
//Even though German and Czech are both high-resource languages in the context of machine translation, though the Czech translations are rated overall higher.
//I intentionally refrain from explaining this using some properties of those languages.
//Rather, it may be the overall quality of the particular machine translation system or its usage for that specific language pair or the result of bias of the evaluation models.
In some cases, the meaning of the metaphor is exemplified through translation, such as in Example 1 in @tab:examples_translation.
In this case, the German translation still contains a metaphor, though the meaning changed from the house being silent to the house being impenetrable.

Over-translating idioms is a well-known problem for language learners #cite("titford1983translation").
In Example 2, the interjection "_shoot_" is a prompt for elaboration.
However, it was translated literally into Czech as "_open fire_" because the overloaded prompt meaning does not exist in that language.
Because of this error, the meaning of the translation is incorrect.
It may happen that one system translates the metaphorical meaning correctly while another one copies the lexical level, such as in Example 3.
The translation of NLLB uses the phrase _"black mood"_ in German, which does not exist in that language and therefore meaning is lost.

#figure(
  [
    #v(5mm)
    
    #box[#image("img/radar/translate_deepl_de.svg", width: 24.5%)]
    #box[#image("img/radar/translate_google_de.svg", width: 24.5%)]
    #box[#image("img/radar/translate_nllb_de.svg", width: 24.5%)]
    #box[#image("img/radar/translate_t5_de.svg", width: 24.5%)]

    #box[#image("img/radar/translate_deepl_cs.svg", width: 24.5%)]
    #box[#image("img/radar/translate_google_cs.svg", width: 24.5%)]
    #box[#image("img/radar/translate_nllb_cs.svg", width: 24.5%)]
    #box[#image("img/radar/translate_t5_cs.svg", width: 24.5%)]
  ],
  caption: [
    Evaluation of translation models on 
    #box(fill: rgb("#9791c6"), inset: 1mm, baseline: 1mm)[literal] (left) and
    #box(fill: rgb("#ccabce"), inset: 1mm, baseline: 1mm)[metaphorical] (right)
    sentences. #v(3mm)
  ],
)
<fig:radar_translation>

#v(1cm)

#figure(
  tablex(
    columns: (auto, 14.3cm),
    align: left + horizon,
    auto-vlines: false,
    repeat-header: true,

    [*Index*], [*Example*],
    align(center)[1], [
      *Source (metaphor)*: _"The house was a tomb."_ #linebreak()
      *NLLB (German)*: _"Das Haus war ein Schloss."_ *(preservation 1, present 4)* #linebreak()
      #h(7mm) *(transcript)*: _"The house was a castle."_ #linebreak()
      *NLLB (Czech)*: _"Dům byl hrob."_ *(preservation 4, present 4)* #linebreak()
      #h(3mm) *(transcript)*: _"The house was a tomb."_ #linebreak()
    ],
    align(center)[2], [
      *Source (metaphor)*: _"You disagree? Ok shoot."_ #linebreak()
      *Source (literal)*: _"You disagree? Ok tell why."_ #linebreak()
      *Google (metaphor)*: _"Nesouhlasíš? Ok střílet."_ *(preservation 2)* #linebreak()
      #h(11.5mm) *(transcript)*: _"You disagree? Ok to shoot."_ #linebreak()
      *Google (literal)*: _"Nesouhlasíš? Ok řekni proč."_ *(preservation 5)* #linebreak()
      #h(6mm) *(transcript)*: _"You disagree? Ok say why.."_ #linebreak()
    ],
    align(center)[3], [
      *Source (metaphor)*: _"You'd better keep away from Bill today because he's in a black mood."_ #linebreak()
      *Google*: _"Du solltest dich heute besser von Bill fernhalten, denn er ist schlecht gelaunt."_ #linebreak()
      #h(0mm) *(trans.)*: _"You should stay away from Bill today because he is in a bad mood."_ #linebreak()
      *NLLB*: _"Du solltest dich besser heute von Bill fernhalten, weil er in einer schwarzen Stimmung ist."_ #linebreak()
      #h(0mm) *(trans.)*: _"You should stay away from Bill today because he is in a black mood."_ #linebreak()
    ],
  ),
  caption: [Examples of translations of FMO sentences. #v(3mm)],
) 
<tab:examples_translation>

#pagebreak()

= Discussion
<sec:end>

The conclusions of particularly the qualitative analysis hint at a deficiency of current NLP systems.
For translation, we can imagine that no qualified human translator would make the same error as in Example 1 in @tab:examples_translation.
However, this disappointment may stem from a confusion regarding the tasks which those systems are solving.
Indeed, those machine translation systems are trained on parallel data which correspond to the output of humans solving the same task (i.e. translation).
However, there are different types of translations #cite("sager1981types", "sager1997text", "sager1998distinguishes"), among others:
- *Translation "word-for-word"*: not considering cultural or linguistic differences.
- *Translation "thought-for-thought"*: conveying the intent or meaning of the text.
- *Transcreation*: _recreating_ the text in the target language (e.g. some types of poetry translations).
- *Localization*: adapting the text to a particular target audience (e.g. using miles instead of kilometres when translating to American English).

#h(1em)
Naturally, different types of translations are needed for various purposes and a similar thing can be said about paraphrasing and other NLP tasks.
It may be the case that the machine translation systems, trained in a supervised manner using forced-decoding on parallel data from human translations, are mixing the translation types due to the data being mixed as well.
Because the task, from the perspective of the NLP systems, is rather unspecified (i.e. _how to translate/paraphrase_), it is not surprising that the systems fail on intentionally difficult inputs (metaphors requiring knowledge of the external world).

Similarly to different agent levels #cite("bisk2020experience"), evaluation of the different types of translations requires different agents.
For example, evaluating the incorrect translation of Example 1 in @tab:examples_translation required some reasoning and knowledge of what _"tomb"_ and _"castle"_ may represent, which relies on the experience of the external world.
Recently, #cite("piantasodi2022meaning", "andreas2022language") argue that, despite the limitation of being only textual, language models can appear to have access to deeper meaning and intentions of texts.
This may be caused by using lexicalized (or _"dead"_) phrases to arrive at this conclusion, which is a methodological error as those can indeed be learned from text.
Nonetheless, the possible limit of intent understanding, needed for "thought-for-thought" translation and paraphrasing, may be sufficient for our NLP tasks.

#v(-4mm)

= Summary

This paper
- framed two NLP tasks (machine translation and paraphrasing) as communication with requirements;
- focused on the problem of accessing deeper meaning of texts, specifically metaphors;
- used a large language model and sentence similarity to evaluate how well the transformations are done using current state-of-the-art systems;
- found very little difference in paraphrasers, which can be caused by having an underspecified task;
- found that the evaluation approach is feasible for machine translation where it uncovers critical errors and verifies the intuition that texts without metaphors are easier to translate.

#text(size: 10pt)[*Limitations and Future Work*]
#v(2mm)

As with all evaluations using closed-source large language models, there is an issue of reproducibility as the particular model may not be supported anymore by OpenAI in several years.
For this reason, also the model outputs and rating are versioned in the attached code repository.
Another issue is that it is unknown what kind of data the particular language model was trained on, which restricts this investigation to treating it as a blackbox textual language model.
It may be the case, that it had access to the publicly available metaphor dataset during training which undermines the presented results.

Usually, language models are used with multiple prompts and decoding temperatures to get more accurate estimates.
For example, while the metaphor presence prompt did not yield the desired results, directly asking ChatGPT to explain a metaphor in particular text resulted in a comprehensive, and correct, answer.
Further examination of metaphor evaluation using large language models, therefore, remains a venue for future work.

Finally, note that the author is not a translatologist.