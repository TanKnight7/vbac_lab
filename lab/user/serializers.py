from django.contrib.auth.models import Group, User
from rest_framework import serializers

ROLE_RANK = {
    "Super Admin": 5,
    "Administrator": 4,
    "Editor": 3,
    "Author": 2,
    "Contributor": 1,
    "Subscriber": 0,
}

PROTECTED_ROLES = {"Super Admin", "Administrator", "Editor", "Author", "Contributor", "Subscriber"}

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "groups"]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        """
        Create and return a new user instance with hashed password.
        """
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])  # Extract groups (many-to-many)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)  # Hash the password
            user.save()
        if groups:
            user.groups.set(groups)  # Set groups using .set() method
        return user
    
    def update(self, instance, validated_data):
        """
        Update and return an existing user instance with hashed password if provided.
        """
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)  # Extract groups (many-to-many)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)  # Hash the password
        
        instance.save()
        
        if groups is not None:  # Only update if groups were provided
            instance.groups.set(groups)  # Set groups using .set() method
        
        return instance

class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field="name"
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "groups"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        groups = validated_data.pop("groups", ["subscriber"])

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        user.groups.set(groups)
        return user
    
    def validate(self, attrs):
        request = self.context["request"]
        creator = request.user

        assigned_groups = attrs.get("groups")

        if not assigned_groups:
            raise serializers.ValidationError({
                "groups": ["At least one role must be assigned."]
            })

        # 🔎 highest role of creator
        creator_roles = creator.groups.values_list("name", flat=True)
        creator_rank = max(
            [ROLE_RANK.get(r, -1) for r in creator_roles],
            default=-1
        )

        # 🔎 highest role being assigned
        assigned_rank = max(
            [ROLE_RANK.get(g.name, -1) for g in assigned_groups]
        )

        if assigned_rank > creator_rank:
            raise serializers.ValidationError({
                "groups": [
                    "You cannot assign a role higher than your own."
                ]
            })

        return attrs

class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field="name",
        required=False
    )

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "groups"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        request = self.context["request"]
        creator = request.user
        instance = self.instance  # user being edited

        # Get highest role of creator
        creator_roles = creator.groups.values_list("name", flat=True)
        creator_rank = max([ROLE_RANK.get(r, -1) for r in creator_roles], default=-1)

        # Get highest role of the user being edited
        target_roles = instance.groups.values_list("name", flat=True)
        target_rank = max([ROLE_RANK.get(r, -1) for r in target_roles], default=-1)

        # Prevent edits if creator rank is lower than target rank
        if creator_rank < target_rank:
            raise serializers.ValidationError(
                "You cannot edit a user whose role is higher than your own."
            )

        # Optional: still validate assigned groups if provided
        assigned_groups = attrs.get("groups")
        if assigned_groups is not None:
            if not assigned_groups:
                raise serializers.ValidationError({
                    "groups": ["Group list cannot be empty if provided."]
                })
            assigned_rank = max([ROLE_RANK.get(g.name, -1) for g in assigned_groups])
            if assigned_rank > creator_rank:
                raise serializers.ValidationError({
                    "groups": ["You cannot assign a role higher than your own."]
                })

        return attrs


    def update(self, instance, validated_data):
        # Update basic fields
        for attr, value in validated_data.items():
            if attr not in ["password", "groups"]:
                setattr(instance, attr, value)

        # Update password only if provided
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()

        # Update groups only if provided
        groups = validated_data.get("groups")
        if groups is not None:
            instance.groups.set(groups)

        return instance

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "groups"]  # fields to display

    def validate(self, attrs):
        """
        Prevent deletion if the requesting user has a lower role than the target user.
        """
        request = self.context["request"]
        creator = request.user
        instance = self.instance

        if not instance:
            raise serializers.ValidationError("User instance not provided.")

        # Highest role of the requester
        creator_roles = creator.groups.values_list("name", flat=True)
        creator_rank = max([ROLE_RANK.get(r, -1) for r in creator_roles], default=-1)

        # Highest role of the target user
        target_roles = instance.groups.values_list("name", flat=True)
        target_rank = max([ROLE_RANK.get(r, -1) for r in target_roles], default=-1)

        # Block deletion if requester rank is lower than target rank
        if creator_rank < target_rank:
            raise serializers.ValidationError(
                {"error":"You cannot delete a user whose role is higher than your own."}
            )

        return attrs

    def delete(self):
        """
        Perform the deletion.
        """
        instance = self.instance
        if instance:
            instance.delete()
        return instance

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

    def validate(self, attrs):
        """
        Prevent deletion or modification of protected roles.
        """
        instance = getattr(self, "instance", None)
        if instance and instance.name in PROTECTED_ROLES:
            raise serializers.ValidationError({
                "name": f"The role '{instance.name}' is protected and cannot be modified or deleted."
            })
        return attrs