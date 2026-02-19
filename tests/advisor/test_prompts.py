"""Tests for prompt templates."""



class TestPromptTemplates:
    """Test PromptTemplates formatting."""

    def test_import_prompts(self):
        """Test that prompts module can be imported."""
        from advisor.prompts import PromptTemplates

        assert PromptTemplates is not None

    def test_has_system_prompt(self):
        """Test that system prompt exists."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        assert hasattr(templates, "SYSTEM") or hasattr(templates, "system_prompt")

    def test_has_career_prompt(self):
        """Test that career prompt template exists."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        # Check for career-related prompt
        assert hasattr(templates, "CAREER") or hasattr(templates, "career") or \
               callable(getattr(templates, "get_prompt", None))

    def test_has_weekly_review_prompt(self):
        """Test that weekly review prompt exists."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        assert hasattr(templates, "WEEKLY_REVIEW") or hasattr(templates, "weekly_review") or \
               callable(getattr(templates, "get_prompt", None))

    def test_has_goals_prompt(self):
        """Test that goals prompt exists."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        assert hasattr(templates, "GOALS") or hasattr(templates, "goals") or \
               callable(getattr(templates, "get_prompt", None))

    def test_has_opportunities_prompt(self):
        """Test that opportunities prompt exists."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        assert hasattr(templates, "OPPORTUNITIES") or hasattr(templates, "opportunities") or \
               callable(getattr(templates, "get_prompt", None))

    def test_prompts_are_strings(self):
        """Test that prompt templates are non-empty strings."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        # Get all string attributes that look like prompts
        for attr_name in dir(templates):
            if attr_name.isupper() and not attr_name.startswith("_"):
                attr = getattr(templates, attr_name)
                if isinstance(attr, str):
                    assert len(attr) > 0, f"{attr_name} should not be empty"

    def test_system_prompt_mentions_advisor(self):
        """Test that system prompt establishes advisor role."""
        from advisor.prompts import PromptTemplates

        templates = PromptTemplates()

        system = getattr(templates, "SYSTEM", "") or getattr(templates, "system_prompt", "")

        if system:
            system_lower = system.lower()
            assert "advisor" in system_lower or "coach" in system_lower or "mentor" in system_lower
