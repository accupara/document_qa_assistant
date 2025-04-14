import logging
from typing import Optional
from config.logging_config import configure_logging
from core.qa_system import QASystem

def main():
    """Main application entry point."""
    # Configure logging
    configure_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Document QA System")
    
    try:
        qa_system = QASystem()
        
        while True:
            try:
                question = input("\nEnter your question (or 'quit' to exit): ").strip()
                
                if question.lower() in ("quit", "exit", "q"):
                    logger.info("User requested to exit the application")
                    break
                
                if not question:
                    print("Please enter a valid question.")
                    continue
                
                # Get answer and citations
                answer_stream, citations = qa_system.answer_question(question)
                
                # Print citations first
                if citations:
                    print("\nRelevant sources:")
                    print(citations)
                    print("\nAnswer:")
                else:
                    print("\nNo relevant sources found. Generating answer based on general knowledge:")
                
                # Stream the answer
                for chunk in answer_stream:
                    print(chunk, end="", flush=True)
                print()  # New line after streaming
            
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit the application.")
                continue
            except Exception as e:
                logger.error(f"Error processing question: {str(e)}")
                print(f"An error occurred: {str(e)}")
    
    except Exception as e:
        logger.critical(f"Fatal error in application: {str(e)}", exc_info=True)
        print(f"A fatal error occurred: {str(e)}")
    
    logger.info("Document QA System shutdown")

if __name__ == "__main__":
    main()