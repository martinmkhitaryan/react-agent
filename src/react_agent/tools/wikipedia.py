import wikipediaapi

from .base import Action, ActionArgument, Tool


class Wikipedia(Tool):
    def __init__(self, language: str = "en") -> None:
        super().__init__(
            name="Wikipedia",
            description="Search Wikipedia for entities and look up keywords in pages",
            actions=[
                Action(
                    name="search",
                    description="Search Wikipedia for the exact entity. Returns first paragraph or similar entities if not found.",
                    arguments=[
                        ActionArgument(
                            name='entity',
                            description='The exact title or name of the article or entity you want to search for.',
                        )
                    ],
                ),
                Action(
                    name="lookup",
                    description="Case-insensitive keyword to scan for within the currently loaded page",
                    arguments=[
                        ActionArgument(
                            name='keyword',
                            description='Keyword to search (e.g., "born").',
                        )
                    ],
                ),
            ],
        )

        self._wiki = wikipediaapi.Wikipedia(
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='ReactAgent/1.0',
        )

        # NOTE: In the produciton code I will keep the context in the agent side (current user interaction context)
        # and pass it to the tools. We also can cache the page itself

        # Simple cache for current page (for development/demo purposes)
        self._current_page = None

    def take_action(self, action_name: str, **kwargs) -> str:
        return getattr(self, f'_action_{action_name}')(**kwargs)

    def _action_search(self, **kwargs) -> str:
        entity = kwargs['entity']

        page = self._wiki.page(entity)
        if page.exists():
            self._current_page = entity
            summary = page.summary
            if summary:
                clean_summary = summary.replace('\n', ' ').strip()
                if len(clean_summary) > 800:
                    clean_summary = clean_summary[:800] + "..."

                return f"Found page for '{entity}': {clean_summary}"
            else:
                return f"Found page for '{entity}' but no summary available. You can try a lookup action to find specific information."
        else:
            similar = self._wiki.search(entity, results=5)
            if similar:
                similar_titles = [s.title for s in similar]
                return f"Could not find exact match for '{entity}'. Similar pages found: {similar_titles}. Try searching for one of these instead."
            else:
                return f"Could not find '{entity}' and no similar pages found. Please try a different search term or rephrase your query."

    def _action_lookup(self, **kwargs) -> str:
        keyword = kwargs['keyword']

        if not self._current_page:
            return "No page currently loaded. Please use a search action first to load a Wikipedia page before looking up keywords."

        page = self._wiki.page(self._current_page)
        if not page.exists():
            return (
                f"Page '{self._current_page}' not found. Please use a valid page title from a previous search action."
            )

        page_text = page.text
        if not page_text:
            return f"Keyword '{keyword}' not found in page '{self._current_page}'. The page content is not available for searching."

        keyword_lower = keyword.lower()
        page_lower = page_text.lower()

        matches = []
        start_idx = 0

        while True:
            start_idx = page_lower.find(keyword_lower, start_idx)
            if start_idx == -1:
                break

            context_start = max(0, start_idx - 200)
            context_end = min(len(page_text), start_idx + len(keyword) + 200)
            context = page_text[context_start:context_end]

            context = context.replace('\n', ' ').strip()
            if context_start > 0:
                context = "..." + context
            if context_end < len(page_text):
                context = context + "..."

            matches.append(context)
            start_idx += 1

        if not matches:
            return f"(Result 0 / 0) No results found for '{keyword}' in page '{self._current_page}'."

        results = []
        for i, match in enumerate(matches, 1):
            results.append(f"(Result {i} / {len(matches)}) {match}")

        return "\n".join(results)
