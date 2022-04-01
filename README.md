<h1 align="center">Movie Reviewer</h1>

<p align="center"> 
<img src='https://user-images.githubusercontent.com/72295771/161219157-d8e0c857-7d88-4338-a128-771d71dccaee.jpg' width="500">
</p>

<p align="center">
  Photo by <a href="https://unsplash.com/@markuswinkler?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Markus Winkler</a> on <a href="https://unsplash.com/s/photos/critic?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
</p>

## Dependencies

- Here, I'm going to install the dependencies that are helping me to build my pipeline. I'm using **Haystack** – it is an **open-source framework** for building search systems that work intelligently over large document collections.

- I wanted to use **ElasticSearch** for saving the documents after finishing the sentiment analysis but instead I made the output saved in **MySQL** or **JSON** file!

- For **Language Detection**, the **seqtolang** library was having an error in reading the length of the sequence while the model is trying to pack padding the sequence of embedding to the LSTMs, I **Pulled** the package, and fixed the issue that occurred. [Repos Link](https://github.com/AI-Ahmed/seqtolang).

---
## Preprocessing

- In the preprocessing, I had to pull the samples you sent to us and start to create synthetic data out of them so that I can simulate the amount of batched data you're going to test the pipeline using it. 

<p align="center">
  <img width="500" src='https://user-images.githubusercontent.com/72295771/161220734-8eabaf93-407a-49ca-b988-8baacd8bb35b.png'>
</p>
<p align="center">Snippet of the <b>synthetic data</b></p>

---

## Building Pipeline

- My Algorithm is based on building **Documents** out of the `review_text`, So that I can create a more rapid and reliable technique using **Hay Stack**. 

- These Documents will allow us to switch from using a query by query to a list of documents with metadata sent to multiple models in one pipeline so that we can have our target (a.k.a sentiment analysis for the reviewed movie(s)), rapidly. My Target was to reduce the cost by increasing efficiency by reducing cost, therefore I built a stacked pipeline that flows the `N` number of documents to get translated and classified then stored into **RDS** or **JSON** file.

<p align="center"><img src='https://i.imgur.com/q5rKysc.png'/></p>

<p align="center">Pipeline Architecture</p>

**Note: In Sentiment Analysis**,

Since it is a movie sentiment analysis, we know that the emotions of watching movies can affect the review of the clients. Therefore, it will be much more efficient to use a text classifier that is based on emotion or trained on emotional text.

<p align="center"><img width="500" src=https://user-images.githubusercontent.com/72295771/161221943-f58e937c-0882-4ee0-aa28-97409ed6427b.png></p>

<p align="center">Snippet of the output process if using <b>JSON</b> format</p>

---

<h1 align="center">Hope you liked it!</h1>

