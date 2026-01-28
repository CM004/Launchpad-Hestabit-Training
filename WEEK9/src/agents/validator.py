from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
from orchestrator.messages import ValidationTask, ValidationResult

class ValidatorAgent(RoutedAgent):
    
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(description="Validator Agent - Quality Assurance")
        self._model_client = model_client
    
    @message_handler
    async def handle_task(self, message: ValidationTask, ctx: MessageContext) -> ValidationResult:
        system_prompt = (
            "You are a Validator Agent responsible for quality assurance.\n\n"
            "Your validation checklist:\n"
            "1. **Accuracy**: Are facts correct? Any hallucinations?\n"
            "2. **Completeness**: Does it fully answer the original question?\n"
            "3. **Logical Consistency**: Are there contradictions?\n"
            "4. **Relevance**: Does it stay on topic?\n"
            "5. **Clarity**: Is the answer clear and well-structured?\n\n"
            "Respond in this format:\n"
            "VALIDATION: [PASS/FAIL]\n"
            "ERRORS: [List any errors found, or 'None']\n"
            "FINAL_RESULT: [Approved result or corrected version]\n")
        
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=(f"Original Task:\n{message.original_task}\n\n"
                    f"Reflected Result to Validate:\n{message.reflected_result}\n\n"
                    f"Perform validation and provide your assessment."),
                source="user")]
        
        # Execute validation with local Qwen model
        model_result = await self._model_client.create(messages)
        validation_text = str(model_result.content)
        is_valid = "fail" not in validation_text.lower()
        
        # Log validation results
        print(f"\n{'='*80}")
        print(f"Validator-{self.id.key}")
        print(f"{'-'*80}")
        print(f"Validation Status: {'PASS' if is_valid else 'FAIL'}")
        
        return ValidationResult(
            is_valid=is_valid,
            final_result=message.reflected_result)