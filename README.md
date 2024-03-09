## Chat with a Document


Slight modifications to DeepLearnin.ai's course "Langchain chat with your data" https://learn.deeplearning.ai/courses/langchain-chat-with-your-data/lesson/1/introduction, this notebook creates a chatbot with my resume (or really any similar style pdf you like). 


Running the App
--------------------

1. In a terminal:
    ```
     python3 -m venv venv && \
     source venv/bin/activate && \
     pip3 install --upgrade pip && \ 
     pip3 install -r requirements.txt
     panel serve app.py --port 5006 --address 0.0.0.0 --allow-websocket-origin=*
     ```
2. Docker pull:
    ```
    docker pull marinert/toddbot:latest
    docker run -p 5006:5006 toddbot:latest
    ```
3. Docker build:
    ```
    docker build . -t toddbot:latest
    docker run -p 5006:5006 toddbot:latest
    ```
4. Go to http://0.0.0.0:5006/app
5. Enter your OpenAI API Key, hit submit.
6. You should now be able to chat with my resume, or upload one of your own!

Modifications
-------------
1. To keep up with usages,

    a. with langchain: qa() is changed to qa.invoke().

    b. with panel: parameter style =() is updated to styles=().

2. To manage dependencies,

    a. chromadb is set to chromadb==0.4.3.
    
    b. Python is 3.11.

3. To adapt the semantic search (addressing retrieval failures),

    a. search type is set to 'similarity' because in a resume, it's possible to do the same thing at different companies.

    b. chunk size is set to 126 with overlap at 12 (~10% of chunk size) since most likely you'll be looking for sentence to sentence comparisons.

    c. chain type is set to "stuff".  The documents are small and there aren't a lot, so this is probably the most efficient use since it will all fit in one prompt. 


Uploading other documents
-------------------------

Document qualities to consider.
The prompt and info you're looking for is phrased short and concise. Something like does 'he have experience with \<xyz\>?' would be a good candidate. Something that might not be so good would be writing a complete paragraph to get back a one word answer.  The chunk size is set to about two-sentence length.

Concerns with other documents.
One possible thing that this chatbot doesn't account for is how the retrieval could return results from other documents. So let's say you upload a document for John Doe, and then ask if he has experience with AWS. Documents from my resume could come up as well.  One way to handle this is using metadata, which I haven't gotten to yet. ...'yet'... :)

Exploring Further
-----------------

1. Search types: similarity v mmr.
2. chain types: stuff, map_reduce, refine.
3. introducing compression just for the sake of demonstrating it.
4. Re-engineering the prompt. The results are pretty bad, and I think some basic prompt engineering will do wonders. 
5. creating panels exploring llm evaluations using rouge and bleu (also more so for comprehension demo purposes), possibly also the RLHF v PPO concepts.
6. introducing open-source models.
7. fine-tuning those os models, exploring more into optimizing them with quantization and distillation.
8. I understand the concept of KL Divergence, but it stops there. I'd like to be able to speak about/implement it intelligently in LLM evaluation.
9. add colors.
10. add testing.
11. develop a pipeline I can actually share.
12. add the multiquery approach.

