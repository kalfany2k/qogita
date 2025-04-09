from app import models, schemas
from app.database import get_db
import codecs
import csv
from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET

router = APIRouter(
    tags=['Products'],
    prefix="/products"
)

@router.post("/csv")
def post_products_from_csv(
    csv_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db.query(models.Product).delete()
    if csv_file.filename.endswith("csv"):
        csvReader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'))
        for row in csvReader:
            try:
                # Validate each row, and replace GTIN & pack_size values to null, since they are not mandatory
                product_data = schemas.CSVInput(
                    product_name=row["Product Title"],
                    price=row["Variant Price"],
                    SKU=row["Variant Sku"],
                    GTIN=row["Variant Barcode"],
                    stock_quantity=row["Variant Inventory Quantity"],
                    pack_size=row["Product.custom.pack_size"]
                )

                # Create the database object
                product_model = models.Product(resource_identifier="csv", brand=None, portfolio=None, volume=None, **product_data.model_dump())

                db.add(product_model)
                db.commit()
            except ValidationError as e:
                print(f'ERROR:Encountered an error for product {row["Product Title"]} in field(s) {", ".join([",".join(error["loc"]) for error in e.errors()])}: {
                    ", ".join([error["msg"] for error in e.errors()])
                }')
                db.rollback()
                continue

@router.post("/xml")
def post_products_from_xml(
    xml_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db.query(models.Product).delete()
    if xml_file.filename.endswith("xml"):
        tree = ET.parse(xml_file.file)
        root = tree.getroot()[1]

        for item in root.findall("item"):
            try:
                product_data = schemas.XMLInput(
                    GTIN=item.find("articleEAN").text,
                    brand=item.find("brand").text,
                    portfolio=item.find("portfolio").text,
                    product_name=item.find("articleName").text,
                    volume=item.find("volume").text,
                    price=item.find("priceWithoutVat").text,
                    stock_quantity=item.find("stockQuantity").text,
                )

                product_model = models.Product(resource_identifier="xml", SKU=None, **product_data.model_dump())

                db.add(product_model)
                db.commit()
            except ValidationError as e:
                print(f'ERROR:Encountered an error for product {item.find("articleName").text} in field(s) {", ".join([",".join(error["loc"]) for error in e.errors()])}: {
                    ", ".join([error["msg"] for error in e.errors()])
                }')
                db.rollback()
                continue