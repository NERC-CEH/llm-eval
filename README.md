# llm-eval
This repository contains a reproducible workflow setup using [DVC](https://dvc.org/) backed by a [JASMIN object store](https://help.jasmin.ac.uk/docs/short-term-project-storage/using-the-jasmin-object-store/). Before working with the repository please contact [Matt Coole](mailto:matcoo@ceh.ac.uk) to request access to the Jasmin object store `llm-eval-o`. Then follow the instructions below.

## Requirements
- [Ollama](https://ollama.com/download) ([`llama3.1`](https://ollama.com/library/llama3.1) and [`mistral-nemo`](https://ollama.com/library/mistral-nemo) models)

## Getting started
First create a new virtual environment and install the required dependencies:
```shell
python -m venv .venv
source .venv/bin/activate
pip install .
```
Next setup your local DVC configuration with your [Jasmin object store access key](https://help.jasmin.ac.uk/docs/short-term-project-storage/using-the-jasmin-object-store/#creating-an-access-key-and-secret):
```shell
dvc remote modify --local jasmin access_key_id '<ACCES_KEY_ID>'
dvc remote modify --local jasmin secret_access_key '<KEY_SECRET>'
```
Pull the data from the object store using DVC:
```shell
dvc pull
```
You should now be ready to re-run the pipeline:
```shell
dvc repro
```
This pipeline is defined in [`dvc.yaml`](dvc.yaml) and can be viewed with the command:
```shell
dvc dag
```
```
                 +----------------+                                        
                 | fetch-metadata |                                        
                 +----------------+                                        
                          *                                                
                          *                                                
                          *                                                
                +------------------+            +-----------------------+  
                | extract-metadata |            | fetch-supporting-docs |  
                +------------------+            +-----------------------+  
                                  **               **                      
                                    ***         ***                        
                                       **     **                           
                                    +------------+                         
                                    | chunk-data |                         
                                    +------------+                         
                                           *                               
                                           *                               
                                           *                               
                                +-------------------+                      
                                | create-embeddings |                      
                                +-------------------+                      
                                           *                               
                                           *                               
                                           *                               
+------------------+            +--------------------+                     
| generate-testset |            | upload-to-docstore |                     
+------------------+            +--------------------+                     
                  **              **                                       
                    ***        ***                                         
                       **    **                                            
                +------------------+                                       
                | run-rag-pipeline |                                       
                +------------------+                                       
                          *                                                
                          *                                                
                          *                                                
                    +----------+                                           
                    | evaluate |                                           
                    +----------+
```

## Notes

### DVC and CML
Notes on the use of Data Version Control and Continuous Machine Learning:
- [DVC](dvc.md)
- [CML](cml.md)

### vLLM
Notes on running models with vLLM:
- [vLLM](vllm.md)