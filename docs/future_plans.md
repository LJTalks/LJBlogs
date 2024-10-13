## Current status

We are keeping each section of the prooject seperate so they can be exported in vaius combinations in future. So the main project level app handles sitewide functions, and each app looks after it's own concerns as as far as possible.

#### Tools to investigate

**GitHub API Overview:**

GitHub's official **REST API** can be used to access data such as user profiles, repositories, and contributions. You can find the documentation here [GitHub REST API Documentation](https://docs.github.com/en/rest?apiVersion=2022-11-28).

There's also a **GraphQL API** that might allow more efficient queries for specific data: [GitHub GraphQL API](https://docs.github.com/en/graphql).

**GitHub Readme Stats**: This project uses the GitHub API to fetch and display contribution streaks in your README file. You can embed it in your website as well.

[Anuraghazra Repo](https://github.com/anuraghazra/github-readme-stats)
Example of the URL for a streak:
html

```
<img src="https://github-readme-streak-stats.herokuapp.com/?user=yourusername" alt="Your GitHub Streak" />
```

This service automatically updates every day, and you can customize it with parameters for appearance.

**Create My Own Banner with API Data**: I would like full control over the streak calculation and display, I plan to work out how to:

_Fetch Daily Contributions_: Use the **GraphQL API** to fetch contribution days, then calculate the streak from the data.

```
{
  user(login: "yourusername") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
```

### Also, does Strava have an API...
