"""Feed category catalog + profile-based matching for onboarding."""

from dataclasses import dataclass, field

MIN_FEEDS = 5


@dataclass
class FeedCategory:
    id: str
    label: str
    icon: str  # lucide icon name
    match_keywords: list[str] = field(default_factory=list)
    feeds: list[dict] = field(default_factory=list)  # [{url, name}]


FEED_CATALOG: list[FeedCategory] = [
    FeedCategory(
        id="ai_ml",
        label="AI / ML",
        icon="brain",
        match_keywords=[
            "ai",
            "ml",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "nlp",
            "natural language",
            "computer vision",
            "llm",
            "large language model",
            "neural network",
            "transformer",
            "gpt",
            "diffusion",
            "generative ai",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/MachineLearning/.rss", "name": "r/MachineLearning"},
            {"url": "https://rss.arxiv.org/rss/cs.AI", "name": "arXiv cs.AI"},
            {"url": "https://rss.arxiv.org/rss/cs.LG", "name": "arXiv cs.LG"},
            {"url": "https://blog.google/technology/ai/rss/", "name": "Google AI Blog"},
        ],
    ),
    FeedCategory(
        id="web_dev",
        label="Web Dev",
        icon="globe",
        match_keywords=[
            "web",
            "frontend",
            "backend",
            "fullstack",
            "full-stack",
            "javascript",
            "typescript",
            "react",
            "vue",
            "angular",
            "next.js",
            "nextjs",
            "svelte",
            "node",
            "nodejs",
            "css",
            "html",
            "django",
            "flask",
            "rails",
            "php",
            "fastapi",
            "express",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/webdev/.rss", "name": "r/webdev"},
            {"url": "https://www.reddit.com/r/javascript/.rss", "name": "r/javascript"},
            {"url": "https://blog.chromium.org/feeds/posts/default", "name": "Chromium Blog"},
        ],
    ),
    FeedCategory(
        id="systems_infra",
        label="Systems / Infra",
        icon="server",
        match_keywords=[
            "systems",
            "infrastructure",
            "distributed",
            "kernel",
            "linux",
            "os",
            "networking",
            "database",
            "postgres",
            "redis",
            "kafka",
            "c",
            "c++",
            "rust",
            "go",
            "golang",
            "performance",
            "low-level",
            "embedded",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/programming/.rss", "name": "r/programming"},
            {"url": "https://www.reddit.com/r/systems/.rss", "name": "r/systems"},
            {"url": "https://www.reddit.com/r/rust/.rss", "name": "r/rust"},
        ],
    ),
    FeedCategory(
        id="security",
        label="Security",
        icon="shield",
        match_keywords=[
            "security",
            "cybersecurity",
            "infosec",
            "pentest",
            "penetration testing",
            "vulnerability",
            "crypto",
            "cryptography",
            "privacy",
            "zero-day",
            "malware",
            "threat",
            "appsec",
            "devsecops",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/netsec/.rss", "name": "r/netsec"},
            {"url": "https://krebsonsecurity.com/feed/", "name": "Krebs on Security"},
            {"url": "https://www.schneier.com/feed/atom/", "name": "Schneier on Security"},
        ],
    ),
    FeedCategory(
        id="startups_vc",
        label="Startups / VC",
        icon="rocket",
        match_keywords=[
            "startup",
            "startups",
            "vc",
            "venture capital",
            "fundraising",
            "saas",
            "founder",
            "entrepreneurship",
            "yc",
            "y combinator",
            "seed",
            "series a",
            "product-market fit",
            "growth",
            "indie hacker",
            "bootstrapping",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/startups/.rss", "name": "r/startups"},
            {"url": "https://news.ycombinator.com/rss", "name": "Hacker News"},
            {"url": "https://feeds.feedburner.com/oreilly/radar/atom", "name": "O'Reilly Radar"},
        ],
    ),
    FeedCategory(
        id="data_science",
        label="Data Science",
        icon="bar-chart",
        match_keywords=[
            "data science",
            "data engineering",
            "analytics",
            "statistics",
            "pandas",
            "spark",
            "etl",
            "data pipeline",
            "visualization",
            "tableau",
            "jupyter",
            "notebook",
            "sql",
            "bigquery",
            "snowflake",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/datascience/.rss", "name": "r/datascience"},
            {"url": "https://www.reddit.com/r/dataengineering/.rss", "name": "r/dataengineering"},
            {"url": "https://rss.arxiv.org/rss/stat.ML", "name": "arXiv stat.ML"},
        ],
    ),
    FeedCategory(
        id="devops_cloud",
        label="DevOps / Cloud",
        icon="cloud",
        match_keywords=[
            "devops",
            "cloud",
            "aws",
            "gcp",
            "azure",
            "kubernetes",
            "k8s",
            "docker",
            "terraform",
            "ci/cd",
            "ci cd",
            "sre",
            "site reliability",
            "monitoring",
            "observability",
            "infrastructure as code",
            "serverless",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/devops/.rss", "name": "r/devops"},
            {"url": "https://www.reddit.com/r/aws/.rss", "name": "r/aws"},
            {"url": "https://www.reddit.com/r/kubernetes/.rss", "name": "r/kubernetes"},
        ],
    ),
    FeedCategory(
        id="mobile",
        label="Mobile",
        icon="smartphone",
        match_keywords=[
            "mobile",
            "ios",
            "android",
            "swift",
            "kotlin",
            "react native",
            "flutter",
            "xamarin",
            "app development",
            "mobile dev",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/iOSProgramming/.rss", "name": "r/iOSProgramming"},
            {"url": "https://www.reddit.com/r/androiddev/.rss", "name": "r/androiddev"},
            {"url": "https://www.reddit.com/r/FlutterDev/.rss", "name": "r/FlutterDev"},
        ],
    ),
    FeedCategory(
        id="general_tech",
        label="General Tech",
        icon="newspaper",
        match_keywords=["tech", "technology", "software", "engineering", "programming"],
        feeds=[
            {"url": "https://news.ycombinator.com/rss", "name": "Hacker News"},
            {"url": "https://www.reddit.com/r/technology/.rss", "name": "r/technology"},
            {"url": "https://www.reddit.com/r/programming/.rss", "name": "r/programming"},
            {"url": "https://lobste.rs/rss", "name": "Lobsters"},
        ],
    ),
    FeedCategory(
        id="open_source",
        label="Open Source",
        icon="git-branch",
        match_keywords=[
            "open source",
            "oss",
            "foss",
            "github",
            "contributing",
            "open-source",
            "linux",
            "free software",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/opensource/.rss", "name": "r/opensource"},
            {"url": "https://github.blog/feed/", "name": "GitHub Blog"},
            {"url": "https://changelog.com/feed", "name": "Changelog"},
        ],
    ),
    FeedCategory(
        id="blockchain_web3",
        label="Blockchain / Web3",
        icon="link",
        match_keywords=[
            "blockchain",
            "web3",
            "crypto",
            "cryptocurrency",
            "ethereum",
            "solidity",
            "defi",
            "nft",
            "smart contract",
            "bitcoin",
            "decentralized",
        ],
        feeds=[
            {"url": "https://www.reddit.com/r/ethereum/.rss", "name": "r/ethereum"},
            {"url": "https://www.reddit.com/r/CryptoTechnology/.rss", "name": "r/CryptoTechnology"},
            {"url": "https://blog.ethereum.org/feed.xml", "name": "Ethereum Blog"},
        ],
    ),
]

_CATALOG_BY_ID: dict[str, FeedCategory] = {c.id: c for c in FEED_CATALOG}


def _tokenize(text: str) -> set[str]:
    """Lowercase and split on common delimiters, keep multi-word phrases too."""
    text = text.lower().strip()
    tokens = set(text.split())
    # Also add the full text as a token for multi-word matching
    tokens.add(text)
    # Add bigrams for multi-word keyword matching
    words = text.split()
    for i in range(len(words) - 1):
        tokens.add(f"{words[i]} {words[i + 1]}")
    return tokens


def match_categories_to_profile(
    interests: list[str] | None = None,
    industries: list[str] | None = None,
    technologies: list[str] | None = None,
    languages: list[str] | None = None,
) -> list[str]:
    """Return category IDs that match profile fields. Always includes general_tech."""
    # Collect all profile text tokens
    profile_tokens: set[str] = set()
    for field_list in (interests, industries, technologies, languages):
        for item in field_list or []:
            profile_tokens |= _tokenize(item)

    matched: list[str] = []
    for cat in FEED_CATALOG:
        if cat.id == "general_tech":
            continue  # always added at end
        for kw in cat.match_keywords:
            if kw in profile_tokens:
                matched.append(cat.id)
                break

    # Always include general_tech
    if "general_tech" not in matched:
        matched.append("general_tech")

    return matched


def feeds_for_categories(category_ids: list[str]) -> list[dict]:
    """Return deduplicated feed list for selected categories."""
    seen_urls: set[str] = set()
    result: list[dict] = []

    for cid in category_ids:
        cat = _CATALOG_BY_ID.get(cid)
        if not cat:
            continue
        for feed in cat.feeds:
            if feed["url"] not in seen_urls:
                seen_urls.add(feed["url"])
                result.append(
                    {
                        "url": feed["url"],
                        "name": feed["name"],
                        "category_id": cid,
                    }
                )

    # Pad to MIN_FEEDS with general_tech if needed
    if len(result) < MIN_FEEDS:
        gt = _CATALOG_BY_ID.get("general_tech")
        if gt:
            for feed in gt.feeds:
                if feed["url"] not in seen_urls:
                    seen_urls.add(feed["url"])
                    result.append(
                        {
                            "url": feed["url"],
                            "name": feed["name"],
                            "category_id": "general_tech",
                        }
                    )
                    if len(result) >= MIN_FEEDS:
                        break

    return result
