from app.application.service.model import Validator


class ValidateAmountToSendUseCase:
    def validate_amount_to_send(self, amount: float) -> bool:
        amount_field_name = "amount to send"
        Validator.validate_number(amount, amount_field_name)
        Validator.is_more_than(amount, 0, amount_field_name)

        return True