import { SkeletonResults } from "./SkeletonResults"
import { formatDateToGovukStyle } from "../utils/date"

function Results({ results, isLoading, searchQuery = "" }) {
  if (isLoading) {
    return <SkeletonResults />
  }

  const highlight = (text) => {
    const regex = new RegExp(searchQuery, "gi")
    const highlightedText = text.replace(regex, (match) => `<mark class="orp-marked-text">${match}</mark>`)
    return { __html: highlightedText }
  }

  const truncateAndHighlightDescription = (description) => {
    const regex = new RegExp(searchQuery, "gi")
    const matchIndex = description.search(regex)

    let truncatedDescription
    if (matchIndex === -1 || matchIndex <= 200) {
      truncatedDescription = description.length > 200 ? description.substring(0, 200) + "..." : description
    } else {
      const start = 0 // Always start from the beginning
      const end = Math.min(description.length, matchIndex + 150) // Include some context after the match
      truncatedDescription = description.substring(start, end) + "..."
    }

    return <span dangerouslySetInnerHTML={highlight(truncatedDescription)} />
  }

  const renderRegulatoryTopics = (topics, searchQuery) => {
    return topics.map((topic, index) => {
      const highlightedTopic =
        searchQuery.length && topic.toLowerCase().includes(searchQuery.toLowerCase()) ? (
          <span dangerouslySetInnerHTML={highlight(topic)} />
        ) : (
          topic
        )

      return (
        <li key={index} className="govuk-body-s orp-secondary-text-colour">
          {highlightedTopic}
        </li>
      )
    })
  }

  return results ? (
    <div className="govuk-summary-list orp-search-results">
      {results.map((result) => {
        const { id, type, title, description, publisher, date_modified, date_valid, regulatory_topics } = result

        // const highlightedTitle = title ? <span dangerouslySetInnerHTML={highlight(title)} /> : ""
        const highlightedDescription = description ? truncateAndHighlightDescription(description) : ""

        // Format the date to the GOV.UK style
        // We're now using the date_valid field instead of date_modified
        const govukDate = date_valid ? formatDateToGovukStyle(date_valid) : "Unknown"

        return (
          <div className="govuk-summary-list__row--no-border" key={id}>
            <span className="govuk-caption-m">{type}</span>
            <h2 className="govuk-heading-m">
              <a href={`/document/${id}`} className="govuk-link">
                {title}
              </a>
            </h2>
            <p className="govuk-body">{highlightedDescription}</p>
            <p className="govuk-body-s orp-secondary-text-colour govuk-!-margin-bottom-2">Published by: {publisher}</p>
            <p className="govuk-body-s orp-secondary-text-colour">Last updated: {govukDate}</p>
            {regulatory_topics && regulatory_topics.length > 0 ? (
              <ul className="govuk-list orp-topics-list">{renderRegulatoryTopics(regulatory_topics, searchQuery)}</ul>
            ) : null}
            <hr className="govuk-section-break govuk-section-break--l govuk-section-break--visible" />
          </div>
        )
      })}
    </div>
  ) : null
}

export { Results }
