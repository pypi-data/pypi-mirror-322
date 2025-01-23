from typing import List

from peewee import DoesNotExist

from heroserver.db import DB
from heroserver.jobmanager.models import Job, SignatureRequest


class ManagerSigning:
    def __init__(self, db: DB):
        self.db = db

    def add_signature_request(self, job_id: int, pubkey: str, signature: str, verified: bool = False) -> SignatureRequest:
        """Add a signature request to a job.

        Args:
            job_id: ID of the job
            pubkey: Public key used for signing
            signature: The signature
            verified: Whether the signature is verified (default: False)

        Returns:
            SignatureRequest: The created signature request instance

        Raises:
            DoesNotExist: If the job_id doesn't exist
        """
        try:
            job = Job.get_by_id(job_id)
            return SignatureRequest.create(job=job, pubkey=pubkey, signature=signature, verified=verified)
        except DoesNotExist:
            raise DoesNotExist(f"Job with ID {job_id} not found")

    def get_signature_requests(self, job_id: int) -> List[SignatureRequest]:
        """Get all signature requests for a job.

        Args:
            job_id: ID of the job

        Returns:
            List[SignatureRequest]: List of signature requests for the job

        Raises:
            DoesNotExist: If the job_id doesn't exist
        """
        try:
            job = Job.get_by_id(job_id)
            return list(SignatureRequest.select().where(SignatureRequest.job == job).order_by(SignatureRequest.date.desc()))
        except DoesNotExist:
            raise DoesNotExist(f"Job with ID {job_id} not found")

    def verify_signature(self, request_id: int) -> bool:
        """Verify a signature request and update the job's signature if verified.

        Args:
            request_id: ID of the signature request to verify

        Returns:
            bool: True if verification successful, False otherwise

        Raises:
            DoesNotExist: If the request_id doesn't exist
        """
        try:
            request = SignatureRequest.get_by_id(request_id)
            # TODO: Implement actual signature verification logic here
            verified = True  # Replace with actual verification

            if verified:
                request.verified = True
                request.save()

                # Update the job's signature field with the verified signature
                job = request.job
                job.signature = request.signature
                job.save()

            return verified
        except DoesNotExist:
            raise DoesNotExist(f"SignatureRequest with ID {request_id} not found")
