from rest_framework import serializers


from ..models.admin import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'request_creator', 'talentee_requested']
        read_only_fields = ['id', 'request_creator']
        depth = 1 

    def create(self, validated_data):
        # Automatically assign the request_creator as the logged-in investigator
        request_creator = self.context['request'].user.investgator
        validated_data['request_creator'] = request_creator
        return super().create(validated_data)


