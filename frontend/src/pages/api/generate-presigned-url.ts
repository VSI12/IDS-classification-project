// pages/api/generate-presigned-url.ts

import type { NextApiRequest, NextApiResponse } from 'next';
import AWS from 'aws-sdk';

// Initialize AWS S3 client
const s3 = new AWS.S3();

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { file_name, file_type } = req.body;

      if (!file_name || !file_type) {
        return res.status(400).json({ error: 'File name and type are required.' });
      }

      // Define the parameters for the presigned URL
      const params = {
        Bucket: process.env.S3_BUCKET_NAME,  // Your S3 Bucket Name
        Key: file_name,  // The file name to upload to S3
        Expires: 60 * 5,  // The URL will be valid for 5 minutes
        ContentType: file_type,  // The MIME type of the file
      };

      // Generate the presigned URL
      const url = await s3.getSignedUrlPromise('putObject', params);

      // Send the URL as a response
      return res.status(200).json({ url });
    } catch (error) {
      console.error('Error generating presigned URL:', error);
      return res.status(500).json({ error: 'Error generating presigned URL' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
