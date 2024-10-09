from rest_framework import serializers


from ..models.admin import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    class Meta:
        model = ContactRequest
        fields = ['id', 'status','created_at','request_creator', 'talentee_requested']
        read_only_fields = ['id', 'request_creator']
        depth = 1 

    def create(self, validated_data):
        # Automatically assign the request_creator as the logged-in investigator
        request_creator = self.context['request'].user.investgator
        validated_data['request_creator'] = request_creator
        return super().create(validated_data)


    def get_status(self,instance):
        if instance.status:
            return 'Accepted'
        return 'Pending'