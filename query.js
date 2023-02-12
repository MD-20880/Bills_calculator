const { Client } = require('@notionhq/client');

const notion = new Client({ auth: process.env.NOTION_API_KEY });

(async () => {
  const databaseId = 'd9824bdc-8445-4327-be8b-5b47500af6ce';
  const response = await notion.databases.query({
    database_id: databaseId,
    filter: {
      or: [
        {
          property: 'In stock',
          checkbox: {
            equals: true,
          },
        },
        {
          property: 'Cost of next trip',
          number: {
            greater_than_or_equal_to: 2,
          },
        },
      ],
    },
    sorts: [
      {
        property: 'Last ordered',
        direction: 'ascending',
      },
    ],
  });
  console.log(response);
})();