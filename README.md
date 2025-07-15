- Artificial Intelligence (AI):
	- Simulation of human intelligence by machines
	- Decision-making, problem-solving, understanding the natural language.
- Machine Learning
	- Learning from data, no explicit programing. Identify patterns, make predictions.
	- Supervised, unsupervised and reinforcement learning.
- Deep Learning
	- Neural networks to automatically learn features from raw data, inspired by structure of the human brain.
- Generative AI
	- Generate new, original content that didn't exist before.
	- Writing text, drawing images, composing music or even generate code.

## What are LLM
Machine learning models specialized in natural language.
Trained to perform tasks such as text generation, summarization, Q&A, translation and more.

Why the LLM are considered large? The number of parameters and the training data, the LLMs contains billions of parameters (GPT-3 has 175 billion).

### Self attention
Models don't just "**read the words**" individually, they understand the context.
### Tokenization
Text is broken into smaller, manageable pieces called token.
Tokens are words, subwords or characters.

The LLMs are self-supervised learning

## Capabilities
- Chat completion and conversational AI
- Text Classification
- Sentiment Analysis
- Embeddings and Semantic Search
- Code Generation

## Uses
- Customer Support and Chatbots
- Content Creation and Copywriting

## Limitations
- **Factual Inaccuracy and Hallucinations:** Made-up facts or fake citations.
- **Lack of Real-Time knowledge:** Models only know up to their las training cycle
- **Limited Context Handling:** Struggle with long-term memory.
- **High computational costs:** Running LLM is expensive

# LLM settings
- **Temperature**: The "creative" or "liberty" of the response
- **Max Tokens**: Max length of the response
- **Stop Sequences**:
- **Top P**
- **Frequency Penalty**
- **Presence Penalty**

## Functions calling in LLM
LLM can trigger external fucntions or APIs
You ask a prompt to the LLM, recognize the intentions and use the tool necessary to complete this action.

## Structured output

Can generate response in a well-defined format like JSON, XML or key-value pairs
This ensure the predictability and consistency. Necessary for API call, automations and data extraction.
Example:
```json
{"city": "city_name", "temperature": "", "conditions": "description"}
```

# Small language models
Are smaller, more efficient and scaled-down version of LLM.
Retain the key functions, like text generation, classification and language understanding, but with significant fewer parameters. This make them faster, cheaper and more efficient to run.

Suitable for real-time apps, mobile or edge computing.

## Use cases
- Edge computing and IoT Devices
- Mobile Applications
- Customer support chatbots
- Offline applications for personalization

# LLM Interaction types
Chat UI for quick and simple task.
API keys for custom and scalable integrations.

# Prompt Engineer
- **Techniques:** Zero-shot, Few-shot, One-shot prompting


## What is a prompt
The prompts are the programs for LLMs, this way we tell to the LLM how we want the answer depending of the input given.

Types of prompts:
- Questions
- Commands
- Fill-in-the-blank
-
### Elements of a Prompt
- Instruction or Task: The core request for the model, a specific task or instruction
- Context
- Input data
- Output format

### Roles of Prompts - System and User Roles
- System Role: Sets up the model's behavior and environment, define the guidelines for the entire conversation.
- User Role: The specific instructions or questions given to the model.

## Prompt Engineering
Crafting and refining prompts to improve model response.

- Help to get more accurate and relevant responses.
- Allow to shape the model's behavior.
- Reduces vague or incorrect outputs.

### Steps of how design effective prompts

1. Start simple: Begin with a simple prompt to know the behavior of the model response.
2. Experiment: try different structures and wording to see how the model's output changes.
3. Iterate: Test and iterate with different inputs.
4. Evaluate: Determine if the prompt has successfully guided model.
5. Templatize: Create a reusable structure for prompts that can be applied to similar tasks.

### Advances prompting techniques
Fine tune interactions for more accurate, meaningful and context aware outputs.
- Zero-shot, One-shot and Few-shot
- Chain-of-Thought
- Role Based and instruction-based
- Contextual prompting with RAG

#### Zero-shot prompting
Simple and most widely used prompting technique.
Provide the model with no prior examples or context before asking it to complete a task.

#### One-shot prompting
Provide one  examples before asking the model to generate a response. Gives the model a bit of direction by showing it a single instance of what you want.
```ad-info
Example:
This blender is perfect for ...

Now, write a description for a coffee maker
```

#### Few-shot prompting
Provide a few examples of the task you want the model to perform before asking it.


#### Chain-of-Thought Prompting
Break down its a thought process and provide a step-by-step explanation. Useful for logical reasoning, problem-solving or multi-step processes.
```ad-info
What is 18/3? Exaplain step by step.
```

#### Instruction-based Prompting
Give the model very clear and direct instructions.

#### Role base prompting
Assign the model a specific role or persona. Helps the model respond with a targeted perspective; doctor; teacher; customer service agent.

### Examples of prompts
```ad-example
You are an AI assistant integrated into an EShop support system.
Your task is to help support agents by summarizing customer support interactions, classifying the ticket type, and evaluating customer sentiment based on the messages exchanged.

Here are the details of a customer support ticket:

- Product: {{product.Model}}
- Brand: {{product.Brand}}
- Ticket Messages: {{ticket.Messages}}

Please perform the following tasks:

1. **Summarization**: Write a detailed summary (up to 30 words) that includes:
    - The current status of the ticket.
    - Any specific questions asked by the customer.
    - What type of response would be most useful from the next support agent.
    - Avoid repeating the product or customer name unless necessary.

2. **Ticket Classification**: Based on the message log, classify the ticket into one of the following categories:
    - Question, Complaint, Feedback, Request for Refund, Product Issue, Other.
    - If the ticket contains multiple categories, choose the most dominant one.

3. **Customer Sentiment Analysis**: Analyze the latest message from the customer and determine their satisfaction level. Focus on the emotional tone of the customer, especially in how they express their needs or frustrations. Provide the satisfaction level using one of the following options:
    - Very Dissatisfied, Dissatisfied, Neutral, Satisfied, Very Satisfied.

Return the output in this structured format (as JSON):


{
  "LongSummary": "string",
  "TicketClassification": "string",
  "CustomerSatisfaction": "string"
}




TEST TICKET LIST
User Message: (show json viewer)
{
  "product": {
    "Model": "XtremeBass 3000",
    "Brand": "SoundTech"
  },
  "Messages": [
    {
      "Sender": "Customer",
      "Message": "I purchased the XtremeBass 3000 headphones last month, and they worked fine for a while. Now, the left earbud is producing no sound at all. I've tried resetting it, but nothing helps. Can you assist me with this issue?"
    },
    {
      "Sender": "Support Agent",
      "Message": "Thank you for reaching out. I'm sorry to hear about your headphones. Can you confirm whether you’ve tried a hard reset or connecting to a different device to rule out a software issue?"
    },
    {
      "Sender": "Customer",
      "Message": "Yes, I’ve already tried connecting it to my phone and laptop. I’ve also tried resetting it twice, but the left earbud is still dead. This is really frustrating."
    }
  ]
}
```

```ad-example
Prompt: Q&A chat on the Ticket Detail Page with Retrieval-Augmented Generation and Citations

You are an AI assistant named 'Assistant' responsible for helping customer service agents handle support tickets for EShop specializing in electronics and computers.

The agent is currently handling the following ticket:

- Product: {{ProductId}}
- Customer: {{CustomerName}}
- Ticket summary: {{TicketSummary}}
- Customer's latest message: {{TicketLastCustomerMessage}}

You will be asked a question related to this ticket. When answering product-related questions, Always search the product manual or relevant documentation to ensure accuracy.

**Citations** are critical in every response. After answering, provide a short, **verbatim** quote from the source to support your reply, using the following format:
- <cite source="manual/document_name">"Exact quote here" (max 10 words)</cite>.

Only include **one citation** per response, and ensure it is directly relevant to the question asked. Your responses should be clear, concise, and professional.



Prompt 2: Q&A Chat Response Text Generator for Customer Communication on the Ticket Detail Page

You are an AI assistant helping a customer support team at EShop, and your task is to draft responses that agents can use to communicate with customers. Based on the customer’s latest message and overall sentiment, generate a suggested response that addresses the customer’s issue, provides helpful guidance, and maintains a friendly tone.

Here are the details:

- **Product**: {{product.Model}}
- **Ticket Summary**: {{request.TicketSummary}}
- **Customer's Latest Message**: {{request.TicketLastCustomerMessage}}

Analyze the sentiment of the customer's latest message and adjust the tone of the response accordingly:
- If the customer appears **frustrated**, include a sympathetic tone and offer reassurance.
- If the customer is **satisfied**, reinforce the positive experience and offer further assistance if needed.

Generate a response that meets the following guidelines:
- Address the customer's specific question or issue.
- Provide clear and concise instructions or solutions.
- Offer a friendly closing statement, inviting the customer to reach out if they need further help.

Return the response in this format:
{
  "Response": "string"
}



TEST TICKET DETAIL

Prompt1: Q&A chat on the Ticket Detail Page with Retrieval-Augmented Generation and Citations
User Message: (show json viewer)
{
  "product": {
    "Model": "UltraView 4K Pro",
    "Brand": "VisionMax"
  },
  "request": {
    "TicketLastCustomerMessage": "Can you guide me on how to adjust the color settings for my UltraView 4K Pro? The colors seem off when I switch to HDMI mode."
  }
}

------------------------------------------------------------------------
Prompt 2: Q&A Chat Response Text Generator for Customer Communication on the Ticket Detail Page
User Message: (show json viewer) -- Customer Ticket 4: Customer Request for Return Policy
{
  "product": {
    "Model": "AirPro Max Blender",
    "Brand": "KitchenMaster"
  },
  "request": {
    "TicketSummary": "Customer inquiring about the return policy for a recently purchased blender.",
    "TicketLastCustomerMessage": "I bought the AirPro Max Blender two weeks ago, and it’s already malfunctioning. It overheats after just 30 seconds of use. Can I return it for a full refund?"
  }
}
```

## Retrieval-Augmented Generation RAG

Enhances the model's ability to generate more accurate and relevant information by integrating external knowledge into the response.

![[Pasted image 20250618144028.png]]

The LLMs are powerful but limited to the data with which was trained.
Combines knowledge with context.

### How Does RAG Work
Ingestion - Building a Knowledge Base
- Collecting Data: Gather information from a wide variety of sources - databases, documents, real-time information from APIS.
- Organizing Information: Need to be organized for easily accessible in the retrieval step. Separate chunks, insert embeddings and create index. Creating numerical representation of documents into vector databases.

Retrieval - Search Relevant Data
- Searching the knowledge Baes
- Identifying Relevant Data
AI isn't just guessing based on its training data, it's pulling from a real-time and proprietary data sources

Generation - Create Coherent Response
- Using Retrieved data
- Combining Knowledge
- Natural Language Output
![[Pasted image 20250619104427.png]]

### Uses Cases
Customer Support and Help Desk
- Provide accurate answer using products manuals and FAQs
Medical and Healthcare Applications
- Access to the last medical research for accurate diagnosis
- Retrieves information from clinical guidelines
Legal Research and Document Retrieval
- Retrieve legal documents, court rulings and case law
- Ensure legal professionals work with accurate and up-to-date legal information.
Financial Services and Market Research
- Provide real-time access to financial market and take decision.

### System complexity
Complex architecture
Latency and response time
- Retrieval process introduce delays when pulling external data.
Cost and Infrastructure Requirements.
- Infrastructure for integrating retrieval and generation can be costly
- Significant computational resources
- Increases context windows
- Ongoing cost for save the data (knowledge)
Data quality and Relevance
- Quality of external data is crucial for accuracy.


## Fine Tuning

Is the process of adapting a pre-trained model to  a specific task. Improve the performance on specialized tasks.

###  Uses cases
Setting the style, tome and format or other qualitative aspects.
Improving reliability at producing a desired output.
Correcting failures to follow complex prompt
Performing a new skill or task that's hard to articulate in a prompt.

### Why fine tuning
The models have general knowledge, but for specific tasks, lack the knowledge for some task, so we need to provide a specific context and tasks to know. Also, the tone, style and how to respond.

Reduce cost, low the latency and more specific answers.

### When fine tuning
Solve a domain-specific problem.
- ***First prompt engineering or RAG before fine tuning.***
```ad-note
Only Fine tuning after try everything and not get the desire result.
```

### How Does fine-tuning works.
1. Domain specific dataset.
2. Train the model, the model keep the general knowledge, but improve in the specific domain.
	1. Adjust the weights and bias
3. Evaluate the model, use validation datasets to pass new knowledge and test the output.
4. Deploy

![[Pasted image 20250619111808.png]]

### Fine tuning methods
1. Full fine-tuning or Instruction fine-tuning
	1. Adjust all the parameters of the pre-trained model
	2. Require large datasets
	3. Provide maximum flexibility and performance for domain specific task
2. Parameter-efficient fine-tuning (PEFT)
	1. Update a small subset of the models parameters.
	2. Require less data and fewer resources
3. Low-Rank Adaptation (LoRA)
	1. Add small trainable matrices to the model layers to learn new tasks
	2. Keep the original model frozen, reducing cost and computational resources
	3. Use smaller datasets without impact the model performance.
4. Transfer learning
	1. Uses when the labeled data is scarce

### Risk
1. Risk of overfitting
	1. Use regularization techs and test
2. Data limitations and quality
	1. limited or biased data reduce the model accuracy
3. Resource requirements
	1. Require a lot of computational resources and time
4. Evolving base models and use cases
	1. Required periodic re-training of fine tuned models.



## Vector DB and Sematic Search with RAGs
Vectors are numerical representation that capture the semantic meaning of data. Indexes and store vectors embeddings for fast retrieval and similarity search.

To know more about vector db please refer to [[Vector DB#Transform unstructured data into vectors - Deep dive]]


### Disk-ANN
Specialized version of ANN designed to operate efficient with vectors stored in disk rather than memory, this uses multi-thread and I/O optimization to access vector data from disk. Also, combine in memory-indexing for a subset of vector with disk-based storage.
- Cost-Effective and Scalable
- Latency and complex: Disk I/O operations can introduce delays.

### Uses cases
- Long-Term Memory for LLMs
	- Storing conversation history as vector embeddings, vector db's enable LLMs to retrieve relevant context dynamically.
		- Personal Assistants, Customer Support.
- Image and Video Search - Similarity Searches
- Media libraries
- E-Commerce
- Semantic search
- Recommendation systems

