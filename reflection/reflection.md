# Application: [Wysa] 

- Most important difference between pipelines: [The main difference between the manual, automated and hybrid pipelines was the amount of input from my own end. Manual being fully created by me, auto created fully by the LLM and hybrid where I revised and edited the LLMs output. This allowed me to understand the utility of each pipeline. Writing each required file took a long time to do and understand yet I beleive the results were good. The auto pipeline was simplest as a script runs everything and creates these files with the LLM but some personas and requirements were not very strong. The hybrid pipeline I believe was the best combination where it takes out the manual generation of each but allows me to go back over and revise and fine tune outputs.]

- Which pipeline produced the clearest personas: [The pipeline that produced the clearest personas was the hybrid pipeline. This is due to the LLM sucessfully generating personas from groups which were grouped in very strong themes. However the persona definition was lacking so the hybrid pipeline allowed for me to edit them to make it more specific and tailored.]

- Which produced the most useful requirements: [The pipeline that produced the most useful requirements was the manual pipeline. This is due to my own control over what works as a requirement, having done many labs now that involved requirement creation I felt that the manual ones are the strongest of all the pipelines.]

- which had the strongest traceability: [All pipelines in their file generation had the previous step where it was generated from correctly traced. That is why all metrics outputs have "1" for tracability ratio. Howwever, the auto pipeline did in some cases miss the mark with what the persona was asking and the requirement generated from that.]

- Most useful pipeline: [The most useful pipeline was the hybrid pipeline. As explained before the hybrid pipeline allowed quick and decently accurate generation of all necessary files, which then just required the fine tuning to keep everything aligned and accuarate] 

- Most surprising finding: [The most suprising finding I encountered came with the auto pipeline. When delivering prompts and expecting certain outputs in json files the LLM had problem with specifics ids and traceability. I opted to manual insert these into each prompt and achieved a much better result but was still suprising.]

- Observed weakness in the automated pipeline: [The biggest observed weakness in the auto pipeline was when generating requirements and tests. The generated test always seemed slightly off from what the main requirement was asking about. Another reason why the hybrid pipeline in a real working sense is probably best.]