"""
SmartScraper Module
"""
import json
from typing import Optional, Any
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.output_parsers.format_instructions import JSON_FORMAT_INSTRUCTIONS

from smart_scraping_agent.llm_friendly_loader import LLMFriendlyWebLoader
from smart_scraping_agent.prompt_factory import *



class SmartScraperAgent:
    def __init__(
            self,
            prompt: str,
            source: str,
            config: dict,
            schema: Optional[BaseModel | Any] = None
            ):
        if config.get("llm").get("temperature") is None:
            config["llm"]["temperature"] = 0

        self.prompt = prompt
        self.source = source
        self.config = config
        self.schema = schema
        self.llm = self._create_llm(config['llm'])

        self.verbose = False if config is None else config.get("verbose", False)
        self.headless = True if self.config is None else config.get("headless", True)
        self.user_agent = self.config.get("user_agent")
        self.loader_kwargs = self.config.get("loader_kwargs", {})
        self.cache_path = self.config.get("cache_path", False)
        self.browser_base = self.config.get("browser_base")
        self.scrape_do = self.config.get("scrape_do")
        
        self.content_type = 'advanced_markdown'

    def get_llm_provider(self, llm_provider):
        match llm_provider:
            case "openai":
                try:
                    from langchain_openai import ChatOpenAI
                    return ChatOpenAI
                except ImportError as e:
                    msg = (
                        "Unable to import from `langchain_openai`."
                        "Please install langchain-openai with "
                        "`pip install -U langchain-openai`."
                    )
                    raise ImportError(msg) from e
                
            case "ollama":
                try:
                    from langchain_ollama import ChatOllama
                    return ChatOllama
                except ImportError as e:
                    msg = (
                        "Unable to import from `langchain_ollama`."
                        "Please install langchain-ollama with "
                        "`pip install -U langchain-ollama`."
                    )
                    raise ImportError(msg) from e
            case "groq":
                try:
                    from langchain_groq import ChatGroq
                    return ChatGroq
                except ImportError as e:
                    msg = (
                        "Unable to import from `langchain_groq`."
                        "Please install langchain-groq with "
                        "`pip install -U langchain-groq`."
                    )
                    raise ImportError(msg) from e
                

    def _create_llm(self, llm_config):
        llm_defaults = {"temperature": 0, "streaming": False}
        llm_params = llm_defaults | llm_config

        if "/" in llm_params["model"]:
            split_model_provider = llm_params["model"].split("/", 1)
            llm_provider = split_model_provider[0]
            llm_params['model'] = split_model_provider[1]
        else:
            msg = ('Please specify the model provider and model name `model: <llm_provider/model_name>` in the llm configuration')
            raise ImportError(msg)
        return self.get_llm_provider(llm_provider)(**llm_params)
    
    def scrape_and_split_content(self):
        loader = LLMFriendlyWebLoader(
                                        urls=[self.source,],
                                        headless=self.headless,
                                        user_agent=self.user_agent,
                                        content_type=self.content_type
                                    )
        return loader.load_and_split()
    
    def get_llm_friendly_text(self):
        loader = LLMFriendlyWebLoader(
                                        urls=[self.source,],
                                        headless=self.headless,
                                        user_agent=self.user_agent,
                                        content_type='basic_markdown'
                                    )
        return loader.load()
    
    def get_format_instruction(self):
        if self.schema:
            try:
                is_schema_validated = issubclass(self.schema, BaseModel)
            except Exception as e:
                print('\n❗ Pease provide a valid `pydantic` schema which is a subclass of `BaseModel` for better results.\n')
                is_schema_validated = False

            if is_schema_validated:
                output_parser = JsonOutputParser(pydantic_object=self.schema)
                format_instructions = output_parser.get_format_instructions()
                # output_parser = JsonOutputParser()
            else:
                format_instructions = JSON_FORMAT_INSTRUCTIONS.format(**{"schema": self.schema})
                output_parser = JsonOutputParser()
        else:
            print('\n⛔ Pease provide a valid `pydantic` schema which is a subclass of `BaseModel` for better results.\n')
            format_instructions = "Follow the user question to generate a valid JSON output and finally wrap the result in `json` tag"
            output_parser = JsonOutputParser()

        return (
                    output_parser,
                    format_instructions
                )

    def get_answer(self,):
        # output_parser = JsonOutputParser() #extract_element
        output_parser, format_instructions = self.get_format_instruction()

        if (additional_info := self.config.get("additional_info")):
            template_no_chunks_prompt = additional_info + TEMPLATE_NO_CHUNKS_MD
            template_chunks_prompt = additional_info + TEMPLATE_CHUNKS_MD
            template_merge_prompt = additional_info + TEMPLATE_MERGE_MD
        else:
            template_no_chunks_prompt = TEMPLATE_NO_CHUNKS_MD
            template_chunks_prompt = TEMPLATE_CHUNKS_MD
            template_merge_prompt = TEMPLATE_MERGE_MD

        max_retries: int = self.config.get('max_retries') or 3
        trial = 1

        while (trial <= max_retries):
            # print(f'Trial: {trial}')

            docs = self.scrape_and_split_content()
            current_page_doc = docs[0]
            chunks = current_page_doc.get('chunks')
            metadata = current_page_doc.get('metadata')
            base_url = metadata.get('base_url')

            if len(chunks) == 1:
                # chunk = chunks[0]
                # prompt = PromptTemplate(
                #     template = template_no_chunks_prompt,
                #     input_variables=["context", "base_url"],
                #     partial_variables= {"format_instructions": format_instructions, "question": self.prompt}
                # )

                # chain = prompt | self.llm | output_parser
                # answer = chain.invoke(chunk)
                # if answer and list(answer.values()):
                #     return answer
                # else:
                self.content_type = "hybrid_markdown"
                trial += 1
                print('\nRetrying ... .. .\n')
            else:
                extract_prompt = PromptTemplate(
                    template = template_chunks_prompt,
                    input_variables=["context", "base_url"],
                    partial_variables= {"format_instructions": format_instructions, "question": self.prompt}
                )
                extract_chain = extract_prompt | self.llm | output_parser

                print('\n🗃️ 🎫 Extracting data from the chunks ... .. .\n')
                if 'openai' in self.config.get('llm', {}).get('model'):
                    batch_results = extract_chain.batch(
                                                            inputs=chunks,
                                                            return_exceptions = True
                                                        )
                else:
                    batch_results = []
                    for idx, chunk in enumerate(chunks):
                        try:
                            answer = extract_chain.invoke(chunk)
                            batch_results.append(answer)
                            print(f'[Result] :: Chunk {idx + 1} :\n{answer}\n\n')
                        except Exception as e:
                            batch_results.append(None)
                            print(f'[Error] :: Chunk {idx + 1} :\n{e.__str__()}\n\n')
                
                if self.verbose:
                    print(f"Batched results ::\n{batch_results}")

                print('\n🗂️ Merging Results ... .. .\n')
                if (merge_function := self.config.get('custom_merge_method')):
                     print(f'Performing custom merging.')
                     answer = merge_function(batch_results)
                else:
                    merge_prompt = PromptTemplate(
                        template = template_merge_prompt,
                        input_variables=["context", "base_url"],
                        partial_variables= {"format_instructions": format_instructions, "question": self.prompt}
                    )
                    merge_chain = merge_prompt | self.llm | output_parser
                    answer = merge_chain.invoke({"context": batch_results, "base_url": base_url})
                    
                if answer:
                    return answer
                else:
                    self.content_type = "hybrid_markdown"
                    trial += 1
                    print('\nRetrying ... .. .\n')
                    
        else:
            raise TimeoutError("\nMax retries completed.\n")

    def execute(self):
        # answer = self.get_answer()
        try:
            answer = self.get_answer()
        except Exception as e:
            error = f"Error :: {e.__str__()}"
            print(f'--{error}')
            answer = error

        return answer
    
    def run(self):
        # answer = self.get_answer()
        try:
            answer = self.get_answer()
        except Exception as e:
            error = f"Error :: {e.__str__()}"
            print(f'--{error}')
            answer = error

        return answer

        